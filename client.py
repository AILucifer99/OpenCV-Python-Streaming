import socket
import cv2
import pickle
import struct
import imutils
import warnings
warnings.filterwarnings('ignore')

camera = False
if camera :
    video = cv2.VideoCapture(0)
else :
    video = cv2.VideoCapture("../sample.mp4")

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_ip_address = "192.168.0.103"

port = 9999
clientSocket.connect((host_ip_address, port))

if clientSocket :
    while (video.isOpened()) :
        try :
            img, frame = video.read()
            frame = imutils.resize(frame, width=480)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            clientSocket.sendall(message)

            #cv2.imshow(f"TO : {host_ip_address}", frame)
            key = cv2.waitKey(10) & 0xFF
            if key == ord('q') :
                clientSocket.close()
        except Exception as e :
            print("VIDEO FINISHED.....")
            break
            
