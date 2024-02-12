'use client';
import Image from 'next/image';
import { useEffect, useRef, useState } from 'react';
import { useRecordWebcam } from 'react-record-webcam';

export default function Home() {
  const {
    activeRecordings,
    createRecording,
    openCamera,
    startRecording,
    stopRecording,
    pauseRecording,
    resumeRecording,
    closeCamera,
    download,
    cancelRecording,
    clearAllRecordings,
    applyRecordingOptions,
  } = useRecordWebcam();

  const [recordingState, setRecordingState] = useState<
    'stop' | 'recording' | 'pause'
  >('stop');
  const webCamRef = useRef<HTMLVideoElement | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const recordDataId = useRef<string>('');
  const inputFileName = useRef<string>('');

  const recordingRef = useRef<null | Awaited<
    ReturnType<typeof createRecording>
  >>();

  const videoControl = useRef<HTMLVideoElement | null>(null);

  const handleOnStop = () => {};

  useEffect(() => {
    return () => {
      Initialise();
    };
  }, []);

  async function Initialise() {
    const recording = await createRecording();
    if (!recording) return;
    recording.mimeType = 'video/webm;codecs=h264';
    recording.fileType = 'webm';

    recordingRef.current = recording;

    await openCamera(recordingRef.current.id);
  }

  async function ButtonRecordControl() {
    if (videoControl.current) {
      const videoControlComponent = videoControl.current;

      if (recordingState == 'recording') {
        videoControlComponent.pause();
        await pauseRecording(recordDataId.current);

        setRecordingState('pause');
      }

      if (recordingState == 'pause') {
        await resumeRecording(recordDataId.current);
      }

      if (recordingState == 'stop') {
        videoControlComponent.currentTime = 0;

        if (recordingRef.current == null) {
          // await Initialise();
        }

        if (recordingRef.current) {
          console.log(recordingRef.current);
          recordDataId.current = recordingRef.current.id;

          await startRecording(recordingRef.current.id);
          console.log(recordingRef.current);
        }
        // mediaRecorderRef.current?.resume();

        videoControlComponent.play();

        setRecordingState('recording');
      }
    }
  }

  async function StopRecordingButtonControl() {
    if (videoControl.current && recordingRef.current) {
      const videoControlComponent = videoControl.current;
      videoControlComponent.currentTime = 0;
      recordingRef.current.fileName = inputFileName.current;
      // console.log(`YES ${inputFileName.current}`);
      await stopRecording(recordingRef.current.id);
      await closeCamera(recordingRef.current.id);
      await download(recordingRef.current.id);
      await cancelRecording(recordingRef.current.id);
      recordingRef.current = null;

      setRecordingState('stop');
      handleOnStop();
      // mediaRecorderRef.current?.stop();

      await Initialise();
    }
  }
  return (
    <main className="flex min-h-screen flex-col items-center justify-between pt-10 pb-24 px-12">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <div className="w-full grid grid-cols-2">
          <div className="col-span-8">
            <div className="py-2 flex justify-center items-center gap-3">
              {recordingState == 'recording' && (
                <div className="w-3 h-3 rounded-full recordingStatus"></div>
              )}
              <input
                className="bg-slate-200 text-slate-800 px-2 py-1"
                placeholder="File name here"
                onChange={(e) => {
                  inputFileName.current = e.target.value;
                }}
              ></input>
            </div>
            <div className="w-full  rounded-2xl overflow-hidden">
              <video
                ref={videoControl}
                width="100%"
                controls={false}
                onEnded={() => {
                  StopRecordingButtonControl();
                }}
              >
                <source src="/HappibotTests.mov" type="video/mp4" />
              </video>

              <video
                className="hidden"
                autoPlay
                playsInline
                muted
                ref={recordingRef.current?.webcamRef}
              ></video>
            </div>

            <div className="text-slate-800 mt-4">
              <button
                onClick={ButtonRecordControl}
                className="bg-gradient-to-b from-yellow-400 to-yellow-600 active:from-yellow-600 active:to-yellow-700 text-slate-50 px-4 py-2"
              >
                {recordingState == 'stop' && 'Record'}
                {recordingState == 'pause' && 'Resume'}
                {recordingState == 'recording' && 'Pause'}
              </button>
              {(recordingState == 'pause' || recordingState == 'recording') && (
                <button
                  onClick={StopRecordingButtonControl}
                  className="bg-gradient-to-b from-red-400 to-red-600 active:from-red-600 active:to-red-700 text-slate-50 px-4 py-2"
                >
                  Stop Recording
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
