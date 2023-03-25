import cv2
 

def VideoPlay(filename):

    #이 파일과 같은 폴더에 있는 비디오 파일을 재생합니다
    capture = cv2.VideoCapture('./' + filename)
    
    while capture.isOpened():
        run, frame = capture.read()
        if not run:
            print("[프레임 수신 불가] - 종료합니다")
            break
        img = cv2.cvtColor(frame, cv2.IMREAD_COLOR)
        cv2.imshow('video', frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    
    capture.release()
    cv2.destroyAllWindows()