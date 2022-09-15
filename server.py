import socket
import cv2
import pickle
import struct
import imutils
import pyshine as ps
import threading
import warnings
warnings.filterwarnings("ignore")

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostName = socket.gethostname()
hostIP = socket.gethostbyname(hostName)

print("HOST IP : {}".format(hostIP))

port = 9999
socketAddress = (hostIP, port)

serverSocket.bind(socketAddress)

serverSocket.listen()
print("Listening at...{}".format(socketAddress))


def show_client(address, client_socket) :
    try :
        print("CLIENT {} CONNECTED...".format(address))
        if client_socket :
            data = b""
            payload_size = struct.calcsize("Q")
            while True :
                while len(data) < payload_size :
                    packet = client_socket.recv(4 * 1024)
                    if not packet : break
                    data = data + packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]

                while len(data) < msg_size :
                    data = data + client_socket.recv(4 * 1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                text = f"CLIENT : {address}"
                frame = ps.putBText(frame, text, 10, 10, vspace=10, hspace=1, font_scale=0.7,
                                    background_RGB=(255, 0, 0), text_RGB=(255, 255, 255))
                cv2.imshow(f"FROM {address}", frame)
                key = cv2.waitKey(10) & 0xFF
                if key == ord('q') :
                    break
            client_socket.close()
    except Exception as e :
        print("CLIENT {} DISCONNECTED...".format(address))
        pass


while True :
    client_socket, addr = serverSocket.accept()
    thread = threading.Thread(target=show_client, args=(addr, client_socket))
    thread.start()
    print("TOTAL CLIENTS : {}".format(threading.activeCount() - 1))

    