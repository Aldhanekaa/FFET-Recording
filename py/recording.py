import cv2 

class Recording:
    cap = None
    recording_state = "stop" # stop, recording, pause
    fileName = "output"
    
    def __init__(self):

        self.fourcc = cv2.VideoWriter_fourcc(*'avc1')
  # Use MP4V codec for MP4 format

    def start(self):
        if self.recording_state  != "recording":
            self.recording_state = "recording"
            # print(self.recording_state)
            self.cap = cv2.VideoCapture(0)
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.out = cv2.VideoWriter(f"{self.fileName}.mov", self.fourcc, fps/2, (int(self.cap.get(3)), int(self.cap.get(4))))  # Adjust parameters as needed


    def resume(self):
        self.recording_state = "recording"

    def pause(self):
        self.recording_state = "pause"

    def runRecording(self):
        if self.recording_state == "recording":
            ret, frame =self.cap.read()
            self.out.write(frame)

    def getRecordingState(self):
        return self.recording_state

    
    def stop_and_saveRecording(self):
        self.cap.release()
        self.out.release()
        self.recording_state = "stop"
    def stop(self):
        self.cap.release()
        self.out.release()
    
    def renameFile(self, fileName):
        self.fileName = fileName


