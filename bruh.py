import cv2

def record_and_save(filename, duration=10, capture_device=0):
    # Open the camera
    cap = cv2.VideoCapture(capture_device)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Couldn't open camera.")
        return

    # Get the frames per second (fps) of the camera
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Example codec (XVID)
    out = cv2.VideoWriter(filename, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

    # Record for the specified duration
    start_time = cv2.getTickCount()
    while (cv2.getTickCount() - start_time) / cv2.getTickFrequency() < duration:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Couldn't read frame.")
            break

        # Display the frame
        cv2.imshow('Recording', frame)

        # Write the frame to the output video file
        out.write(frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release everything when done
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Video saved as '{filename}'")

if __name__ == "__main__":
    # Specify the output filename and duration in seconds
    output_filename = "output.avi"
    recording_duration = 10  # Adjust as needed

    # Record and save the video
    record_and_save(output_filename, duration=recording_duration)