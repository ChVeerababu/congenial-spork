import cv2
import time
import requests,json

def sendtoserver(frame):
    imencoded = cv2.imencode(".jpg", frame)[1]
    file = {'image': ('image.jpg', imencoded.tostring(), 'image/jpeg', {'Expires': '0'})}
    s = time.time()
    response = None
    try:
        response = requests.post('http://10.0.2.235:5000', files=file, timeout=5)
    except Exception as ex:
        print(ex)
        j = [{'emotion': None, 'coordinate': [0, 0, 0, 0], 'age': None, 'gender': None}]
    else: 
        j = response.json()
    finally:
        e = time.time()
        return j,round(e - s,2)

vid = cv2.VideoCapture("rtsp://admin:xx2317xx2317@10.0.2.251:554/Streaming/Channels/102?transportmode=unicast&profile=Profile_2")

while(True):
    ret, frame = vid.read()
    result = sendtoserver(frame)
    print(result)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
