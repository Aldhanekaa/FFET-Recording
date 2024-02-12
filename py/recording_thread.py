from recording import Recording
import threading

class RecordingThread(threading.Thread):
    def __init__(self):
        super(RecordingThread, self).__init__()
        self.instance = Recording()

    def run(self):
        print("RUNNING!")
        # Call methods or perform actions using the MyClass instance
        # while True:
        self.instance.runRecording()

    def start_recording(self):
        return self.instance.start()
        
    def resume(self):
        return self.instance.start()

    def pause(self):
        return self.instance.start()

    def runRecording(self):
        return self.instance.runRecording()

    def getRecordingState(self):
        return self.instance.getRecordingState()

    
    def stop_and_saveRecording(self):
        print("SAVING")
        return self.instance.stop_and_saveRecording()

    def stop(self):
        return self.instance.stop()
    
    def renameFile(self, fileName):
        return self.instance.renameFile(fileName=fileName)