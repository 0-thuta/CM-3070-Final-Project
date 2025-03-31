import unittest
from unittest.mock import patch, MagicMock
from pygrabber.dshow_graph import FilterGraph
import cv2

def get_camera_id_and_names(cameras):
    camera_data = []
    for idx in range(len(cameras)):
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            camera_data.append({
                'camera_id': idx,
                'camera_name': cameras[idx]
            })
        cap.release()
    return camera_data

class TestCameraFunctions(unittest.TestCase):

    @patch.object(FilterGraph, 'get_input_devices', return_value=['Camera 1', 'Camera 2', 'Camera 3'])
    @patch('cv2.VideoCapture')
    def test_get_camera_id_and_names(self, MockVideoCapture, mock_get_input_devices):
        mock_capture = MagicMock()
        mock_capture.isOpened.return_value = True
        MockVideoCapture.return_value = mock_capture

        camera_data = get_camera_id_and_names(['Camera 1', 'Camera 2', 'Camera 3'])
        expected_result = [
            {'camera_id': 0, 'camera_name': 'Camera 1'},
            {'camera_id': 1, 'camera_name': 'Camera 2'},
            {'camera_id': 2, 'camera_name': 'Camera 3'}
        ]
        
        self.assertEqual(camera_data, expected_result)

        MockVideoCapture.assert_any_call(0)
        MockVideoCapture.assert_any_call(1)
        MockVideoCapture.assert_any_call(2)

if __name__ == '__main__':
    unittest.main()
