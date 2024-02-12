import cv2
from recording import Recording
 
vid = cv2.VideoCapture('./video.mp4')
vid_fps = vid.get(cv2.CAP_PROP_FPS)
recording = Recording()
shownFrame = None

fps = int((1/60)*1000)
pause_video = False

while True:
    recording.runRecording()
    # i
    if pause_video is False:
        r, shownFrame = vid.read()
        if not r:
            break
        cv2.imshow("Video", shownFrame)

    k = cv2.waitKey(fps)

    # record and resume key
    if k == ord('r'):
        recording.start()

        if pause_video is True:
            recording.resume()
        pause_video =False

        

        print("Start Recording / Resuming")
        # pass

    # pause key
    if k == ord('p'):
        pause_video = True
        recording.pause()
        # pause the recording and video
        pass

    # recording.runRecording()

    # stop recording & save the file key 
    if k == ord("s"):
        recording.stop_and_saveRecording()



    if cv2.waitKey(1) == ord('q'):
        break


        

cv2.destroyAllWindows()
