import socket
import cv2
import numpy as np
import struct

from .handshake import Handshake 

class CameraStreamer:
    def __init__(self, device_id, server_address, server_port, max_disconnect_count=3):
        self.id = device_id
        self.server_address = server_address
        self.server_port = server_port
        self.max_disconnect_count = max_disconnect_count
        self.handshake = Handshake()

    def receive_frame_size(self, client_socket):
        try:
            frame_size_data = client_socket.recv(struct.calcsize("I"))
            if not frame_size_data:
                return None
            frame_size = struct.unpack("I", frame_size_data)[0]
            return frame_size
        except socket.error as e:
            print(f"[ERROR] Exception occurred while receiving frame size: {repr(e)}")
            return None

    def receive_frame_data(self, client_socket):
        frame_data = b""
        remaining_bytes = self.receive_frame_size(client_socket)
        try:
            while remaining_bytes > 0:
                chunk = client_socket.recv(min(512, remaining_bytes))
                if not chunk:
                    return None
                frame_data += chunk
                remaining_bytes -= len(chunk)
            return frame_data
        except socket.error as e:
            print(f"[ERROR] Exception occurred while receiving frame data: {repr(e)}")
            return None

    def generate_frames(self, data):
        a = data.find(b'\xff\xd8')
        b = data.find(b'\xff\xd9')

        if a != -1 and b != -1:
            jpg = data[a:b + 2]
            data = data[b + 2:]
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                frame = buffer.tobytes()
                return frame

    def establish_connection(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            try:
                client.connect((self.server_address, self.server_port))
                self.handshake.perform_handshake(client, self.id)
                disconnect_count = 0  # 計算斷線次數
                while disconnect_count < self.max_disconnect_count:
                    try:
                        client.sendall('V'.encode('utf-8') + self.handshake.session_key())
                        frame_data = self.receive_frame_data(client)
                        frame = self.generate_frames(frame_data)
                        yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                        disconnect_count = 0  # 重置斷線計數
                    except Exception as e:
                        print(f"[ERROR] Exception occurred: {repr(e)}")
                        disconnect_count += 1
            except socket.error as e:
                print(f"[ERROR] Exception occurred: {repr(e)}")
            finally:
                client.close()