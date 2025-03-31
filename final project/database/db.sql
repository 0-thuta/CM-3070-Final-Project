-- Active: 1743147653217@@127.0.0.1@3306@survsys
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50),
    gmail VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Camera Table
CREATE TABLE Camera (
    camera_id INT PRIMARY KEY AUTO_INCREMENT,
    camera_index INT NOT NULL,
    camera_model VARCHAR(100),
    camera_zone VARCHAR(50),
    zone_x1 INT,
    zone_y1 INT,
    zone_x2 INT,
    zone_y2 INT,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Create Video Table
CREATE TABLE Video (
    video_id INT PRIMARY KEY AUTO_INCREMENT,
    video_name VARCHAR(100),
    video_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    video_location VARCHAR(100),
    video_description TEXT,
    user_id INT NOT NULL,
    camera_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (camera_id) REFERENCES Camera(camera_id)
);

-- Insert sample data into Users table
INSERT INTO users (username, password, role, gmail)
VALUES ('admin', 'password', 'admin', 'admin@gmail.com');

-- Insert sample data into Camera table
INSERT INTO Camera (camera_index, camera_model, camera_zone, zone_x1, zone_y1, zone_x2, zone_y2, user_id)
VALUES (1,'HD Webcam', 'Tester', 0, 0, 540, 1080, 1);

-- Insert sample data into Video table
INSERT INTO Video (video_name, video_description, user_id, camera_id, video_location, video_timestamp)
VALUES 
('intrusion_20240917_064457.mp4', 'Intrusion detected', 1, 1, 'static/intrusions videos/intrusion_20240917_064457.mp4', '2024-09-17 06:44:57'),
('intrusion_20250131_012357.mp4', 'Intrusion detected', 1, 1, 'static/intrusions videos/intrusion_20250131_012357.mp4', '2025-01-31 01:23:57'),
('intrusion_20250319_052357.mp4', 'Intrusion detected', 1, 1, 'static/intrusions videos/intrusion_20250319_052357.mp4', '2025-03-19 05:23:57'),
('intrusion_20250331_062357.mp4', 'Intrusion detected', 1, 1, 'static/intrusions videos/intrusion_20250331_062357.mp4', '2025-03-31 06:23:57');


DROP TABLE IF EXISTS Video;
DROP TABLE IF EXISTS Camera;
DROP TABLE IF EXISTS users;