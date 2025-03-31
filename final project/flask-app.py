from flask import Flask, Response, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import cv2
from ultralytics import YOLO
from pygrabber.dshow_graph import FilterGraph
from threading import Thread
from collections import deque
import pythoncom
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from flask_mail import Mail, Message

#yolo model
yolo = YOLO('yolov8s.pt')

app_secret_key = 'c56fdf3d53fed2d539c7b4d23515'
app = Flask(__name__)

app.config['SECRET_KEY'] = app_secret_key
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'uudd1r1rBAS#'
app.config['MYSQL_DB'] = 'survsys'

mysql = MySQL(app)

class User(UserMixin):
    def __init__(self, user_id, username, gmail, role):
        self.id = user_id
        self.username = username
        self.gmail = gmail
        self.role = role

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    if user:
        return User(user['user_id'], user['username'],user['gmail'],user['role'])
    return None

@app.route('/')
@login_required
def home():
    return render_template('index.html', username=current_user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            login_user(User(user['user_id'], user['username'], user['gmail'], user['role']))
            return redirect(url_for('home'))
        else:
            return render_template('login.html', errorMessage="Invalid username or password")

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['name']
        gmail = request.form['gmail']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE gmail = %s", (gmail,))
        user = cursor.fetchone()

        if user:
            return render_template('register.html', errorMessage="Email already in use. Please log in.")

        cursor.execute("INSERT INTO users (username, gmail, password) VALUES (%s, %s, %s)", 
                       (username, gmail, password))
        mysql.connection.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

last_email_time = None
def send_email(user_email, subject, body):
    sender_email = "camerasurveillancesys2025@gmail.com"
    sender_password = "intrusionalert"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, user_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

def insert_video_into_db(camera_id, video_filename,user_id):
    video_name = os.path.basename(video_filename)
    video_description = 'Intrusion detected at ' + str(datetime.now())
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO Video (video_name, video_location, video_description, user_id, camera_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (video_name, video_filename, video_description, user_id, camera_id))
        mysql.connection.commit()
        cursor.close()

@app.route('/viewcameras/<int:camera_id>/<int:camera_index>/<int:zone_x1>/<int:zone_y1>/<int:zone_x2>/<int:zone_y2>')
@login_required
def viewcameras(camera_id, camera_index, zone_x1, zone_y1, zone_x2, zone_y2):
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        return "Error: Unable to open video stream."
    if not os.path.exists('static/intrusions videos'):
        os.makedirs('static/intrusions videos')

    video_capture = None
    video_filename = None
    intrusion_detected = False

    def generate_frames(user_id,user_gmail):
        nonlocal intrusion_detected, video_capture, video_filename
        global last_email_time
        start_time = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (960, 540))
            cv2.rectangle(frame, (zone_x1, zone_y1), (zone_x2, zone_y2), (0, 0, 255), 2)

            results = yolo.track(frame, stream=True, verbose=False)
            for result in results:
                classes_names = result.names
                for box in result.boxes:
                    if box.conf[0] > 0.4:
                        cls = int(box.cls[0])

                        if cls == 0:
                            x1, y1, x2, y2 = map(int, box.xyxy[0])

                            if (x1 < zone_x2 and y1 < zone_y2 and x2 > zone_x1 and y2 > zone_y1):
                                intrusion_detected = True
                                cv2.putText(frame, 'Intruder detected', (50, 50),
                                            cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)

                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            cv2.putText(frame, f'{classes_names[cls]} {box.conf[0]:.2f}',
                                        (x1, y1), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)

            if intrusion_detected and video_capture is None:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                video_filename = os.path.join('static', 'intrusions videos', f'intrusion_{datetime.now().strftime("%Y%m%d_%H%M%S")}.mp4')
                video_capture = cv2.VideoWriter(video_filename, fourcc, 20.0, (960, 540))

                start_time = datetime.now()


                if last_email_time is None or (datetime.now() - last_email_time).seconds >= 1800:
                    send_email(user_gmail, "Intrusion Alert", "An intrusion was detected on your camera.")
                    last_email_time = datetime.now() 

            if video_capture is not None:
                video_capture.write(frame)

                if (datetime.now() - start_time).seconds >= 20:
                    video_capture.release()
                    video_capture = None
                    intrusion_detected = False
                    insert_video_into_db(camera_id, video_filename, user_id)

            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                break

            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate_frames(current_user.id,current_user.gmail), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed/<int:camera_id>')
def video_feed(camera_id):
    def gen(camera_id):
        cap = cv2.VideoCapture(camera_id)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (640, 480))
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        cap.release()

    return Response(gen(camera_id), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/setcamera')
@login_required
def setcamera():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Camera WHERE user_id = %s", (current_user.id,))
    cameras = cursor.fetchall()
    return render_template('setcamera.html', cameras=cameras)

@app.route('/list_cameras')
def list_cameras():
    pythoncom.CoInitialize()
    graph = FilterGraph()
    cameras = graph.get_input_devices()
    camera_data = []
    for idx in range(len(cameras)):
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            camera_data.append({
                'camera_id': idx,
                'camera_name': cameras[idx]
            })
            print(f"Camera {idx} found: {cameras[idx]}")
        cap.release()
    return camera_data

@app.route('/addcamera')
def addcamera():
    camera_list = list_cameras()
    print(camera_list)
    return render_template('addcamera.html', cameras = camera_list)

@app.route('/addcameras', methods=['POST'])
@login_required
def addcameras():
    camera_index = request.form['camera_index']
    camera_model = request.form['camera_model']
    camera_zone = request.form['camera_zone']
    zone_x1 = request.form['zone_x1']
    zone_y1 = request.form['zone_y1']
    zone_x2 = request.form['zone_x2']
    zone_y2 = request.form['zone_y2']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        INSERT INTO Camera (camera_index,camera_model, camera_zone, zone_x1, zone_y1, zone_x2, zone_y2, user_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (camera_index,camera_model, camera_zone, zone_x1, zone_y1, zone_x2, zone_y2, current_user.id))
    
    mysql.connection.commit()

    flash('Camera added successfully!', 'success')
    return redirect(url_for('setcamera'))

@app.route('/editcamera/<int:camera_id>', methods=['GET', 'POST'])
@login_required
def editcamera(camera_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute("SELECT * FROM Camera WHERE camera_id = %s AND user_id = %s", (camera_id, current_user.id))
    camera = cursor.fetchone()

    if camera is None:
        flash("Camera not found or you do not have permission to edit it.", 'danger')
        return redirect(url_for('setcamera'))


    if request.method == 'POST':

        camera_model = request.form['camera_model']
        camera_zone = request.form['camera_zone']
        zone_x1 = request.form['zone_x1']
        zone_y1 = request.form['zone_y1']
        zone_x2 = request.form['zone_x2']
        zone_y2 = request.form['zone_y2']


        cursor.execute("""
            UPDATE Camera
            SET camera_model = %s, camera_zone = %s,
                zone_x1 = %s, zone_y1 = %s, zone_x2 = %s, zone_y2 = %s
            WHERE camera_id = %s AND user_id = %s
        """, (camera_model, camera_zone, zone_x1, zone_y1, zone_x2, zone_y2, camera_id, current_user.id))


        mysql.connection.commit()
        return redirect(url_for('setcamera')) 


    return render_template('editcamera.html', camera=camera)

@app.route('/deletecamera/<int:camera_id>', methods=['POST'])
@login_required
def delete_camera(camera_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM Camera WHERE camera_id = %s AND user_id = %s", (camera_id, current_user.id))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('setcamera'))

@app.route('/videos')
def videos():
    current_user_id = current_user.id
    

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Video WHERE user_id = %s", [current_user_id])
    videos = cursor.fetchall()
    
    intrusion_videos = {}

    for video in videos:
        video_name = video['video_name']
        video_timestamp = video['video_timestamp']
        video_location = video['video_location']
        video_camera = video['camera_id']
        

        date = video_timestamp.strftime('%B %Y')
        if date not in intrusion_videos:
            intrusion_videos[date] = []
        
        intrusion_videos[date].append({
            'video_name': video_name,
            'video_camera': video_camera,
            'video_location': video_location,
            'video_timestamp': video_timestamp
        })
    
    return render_template('viewvideos.html', intrusion_videos=intrusion_videos)

@app.route('/view_video/<video_name>')
def view_video(video_name):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Video WHERE video_name = %s", [video_name])
    video = cursor.fetchone()
    
    if video:
        return render_template('videoplayer.html', video=video)
    else:
        return "Video not found", 404

if __name__ == '__main__':
    app.run(debug=True, threaded = True)
