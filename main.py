import cv2
import tkinter as tk
import time
import imageio
import datetime 
from recording import Recording
from PIL import Image, ImageTk

global pause_video
global movie_frame
global recordControlBtn

def with_opencv(filename):
    video = cv2.VideoCapture(filename)

    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)

    seconds = round(frame_count / fps) 
    duration = datetime.timedelta(seconds=seconds) 


    return duration, frame_count, fps


video_name = "./video.mp4"
video = imageio.get_reader(video_name)
duration, frame_count, fps = with_opencv(video_name)
print(fps)
recording = Recording()
recorded_fileName = ""


def video_frame_generator():
    def current_time():
        return time.time()

    start_time = current_time()
    _time = 0
    for frame, image in enumerate(video.iter_data()):

        # turn video array into an image and reduce the size
        image = Image.fromarray(image)
        image.thumbnail((750, 750), Image.LANCZOS)

        # make image in a tk Image and put in the label
        image = ImageTk.PhotoImage(image)

        # introduce a wait loop so movie is real time -- asuming frame rate is 24 fps
        # if there is no wait check if time needs to be reset in the event the video was paused
        _time += 1/600
        run_time = current_time() - start_time
        while run_time < _time:
            run_time = current_time() - start_time
        else:
            if run_time - _time > 0.1:
                start_time = current_time()
                _time = 0

        yield frame, image, run_time


def _pause():
    global pause_video
    pause_video = True


def _resume():
    global pause_video
    pause_video = False

def _reset():
    global movie_frame
    movie_frame = video_frame_generator()

if __name__ == "__main__":

    root = tk.Tk()
    root.title('Video in tkinter')

    test_video = tk.Label(root)
    test_video.pack()
    
    movie_frame = video_frame_generator()

    tk.Button(root, text='RESET', command=_reset).pack(side=tk.LEFT)
    tk.Button(root, text='pause', command=_pause).pack(side=tk.LEFT)
    tk.Button(root, text='resume', command=_resume).pack(side=tk.LEFT)
    entry = tk.Entry(root, textvariable=recorded_fileName)

    recordcontrolbtn_text = tk.StringVar()
    recordcontrolbtn_text.set("Start Recording")

    stoprecordcontrolbtn_text = tk.StringVar()
    stoprecordcontrolbtn_text.set("disabled")

    def on_submit():
        user_input = entry.get()
        recording.renameFile(user_input)


    # Create a button to submit the entered text
    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.pack(side=tk.RIGHT)

    durationText = tk.Label(root, text="Loading..")
    durationText.pack(side=tk.BOTTOM)

    entry.pack(side=tk.RIGHT, padx=4)

    def _recordBtnControl():
        global pause_video

        # print(recordControlBtn)
        text = recordControlBtn["text"]
        recording_state = recording.getRecordingState()
        print(f"recording_state {recording_state}")
        if recording_state == "stop":
            _resume()
            _reset()
            recording.start()
        elif recording_state == "recording":
            pause_video = True
            recording.pause()
        elif recording_state == "pause":
            recording.resume()
            pause_video = False

        
        recording_state = recording.getRecordingState()
        if recording_state == "recording":
            stopRecordControlBtn["state"] = "normal"
            recordControlBtn["text"]="Pause Recording"
        elif recording_state == "pause":
            stopRecordControlBtn["state"] = "normal"
            recordControlBtn["text"]="Resume Recording"

    def _stopRecording():
        stopRecordControlBtn["state"] = "disabled"
        recordControlBtn["text"]="Start Recording"
        recording.stop_and_saveRecording()

    recordControlBtn = tk.Button(root, text="Start Recording", command=_recordBtnControl)
    recordControlBtn.pack(side=tk.RIGHT)
    stopRecordControlBtn = tk.Button(root, text="Stop Recording", command=_stopRecording, state="disabled")
    stopRecordControlBtn.pack(side=tk.RIGHT)
    
    # recordingControl.configure(text=)
    pause_video = False


    def on_close():
        root.destroy()
        recording.stop()
        return

    root.protocol("WM_DELETE_WINDOW", on_close)

    startRunning = None
    runningDuration = 0

    while True:
        if not pause_video:
            recording.runRecording()
            recording_state = recording.getRecordingState()

            if recording_state == "stop":
                pass
            elif recording_state == "recording":
                if startRunning is None:
                    startRunning = time.time()
                
                if startRunning is not None:
                    currentTime = time.time()
                    runningDuration = round(currentTime - startRunning)

            try:
                frame_number, frame, run_time = next(movie_frame)
                test_video.config(image=frame)
                root.update()
                durationText["text"] = f"{datetime.timedelta(seconds=runningDuration) } / {duration}"
                
            except:
                _reset()

            # my_label.config(image=frame)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     root.destroy()
        #     recording.stop()
        #     break
    root.mainloop()
