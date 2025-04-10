import React, { memo, useState, useRef } from 'react';
import { useDispatch } from 'react-redux';
import { Sun, Thunder, Warning } from '../../assets';
import { livePrompt } from '../../redux/messages';
import './style.scss';
import { io } from "socket.io-client";

const New = memo(() => {
  const dispatch = useDispatch();
  const [isRecording, setIsRecording] = useState(false);
  const [audioData, setAudioData] = useState([]);
  const [isPanelOpen, setIsPanelOpen] = useState(false);
  const [transcribedText, setTranscribedText] = useState([]);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const animationFrameRef = useRef(null);

  const [socket, setSocket] = useState(null);

  const startRecording = () => {
    setIsRecording(true);
    audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
    navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
      const source = audioContextRef.current.createMediaStreamSource(stream);
      analyserRef.current = audioContextRef.current.createAnalyser();
      source.connect(analyserRef.current);
      visualizeAudio();
      setIsPanelOpen(true);

      // Initialize and connect socket
      if (!socket) {
        const newSocket = io("http://localhost:5001");
        setSocket(newSocket);

        newSocket.on("connect", () => {
          console.log("Connected to the server!");
          newSocket.emit("speech", { duration: 5 });
        });

        newSocket.on("transcription", (data) => {
          console.log("User said:", data.text);
          setTranscribedText((prev) => [...prev, `User: ${data.text}`]);
        });

        newSocket.on("llm_response", (data) => {
          console.log("Llama Model Response:", data.response);
          setTranscribedText((prev) => [...prev, `Bot: ${data.response}`]);
        });

        newSocket.on("audio", (data) => {
          console.log("Playing:", data.audio_file);
        });
      }
    });
  };

  const stopRecording = () => {
    setIsRecording(false);
    cancelAnimationFrame(animationFrameRef.current);
    audioContextRef.current.close();
    setIsPanelOpen(true);
  };

  const visualizeAudio = () => {
    const bufferLength = analyserRef.current.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    const draw = () => {
      analyserRef.current.getByteFrequencyData(dataArray);
      setAudioData([...dataArray]);
      animationFrameRef.current = requestAnimationFrame(draw);
    };
    draw();
  };

  return (
    <div className='New'>
      <div>
        <h1 className='title currentColor'>Dialo</h1>
      </div>
      <div className='audio-sec'>
        {!isRecording ? (
          <button className="call-button" onClick={startRecording}>
            📞
          </button>
        ) : (
          <div className="audio-recorder-panel">
            <div className="audio-graph">
              {audioData.map((value, index) => (
                <div
                  key={index}
                  style={{
                    height: `${value / 2}px`,
                    width: '2px',
                    background: '#16a34a',
                    display: 'inline-block',
                    margin: '0 1px',
                  }}
                ></div>
              ))}
            </div>
            <div className="audio-controls">
              <button onClick={stopRecording} className="end">
                End
              </button>
            </div>
          </div>
        )}
      </div>
      <div className="flex">
        <div className='inner'>
          <div className='card'>
            <Sun />
            <h4 className='currentColor'>Examples</h4>
          </div>

          <div className='card card-bg hover' onClick={() => {
            dispatch(livePrompt("What is my order status?"))
          }}>
            <p className='currentColor'>"What is my order status?" →</p>
          </div>

          <div className='card card-bg hover' onClick={() => {
            dispatch(livePrompt("When can I expect my order to be delivered?"))
          }}>
            <p className='currentColor'>"When can I expect my order to be delivered?" →</p>
          </div>

          <div className='card card-bg hover' onClick={() => {
            dispatch(livePrompt("Can you help me with the top electronic deals of the day"))
          }}>
            <p className='currentColor'>"Can you help me with the top electronic deals of the day" →</p>
          </div>

        </div>

        <div className='inner'>
          <div className="card">
            <Thunder />
            <h4 className="currentColor">Capabilities</h4>
          </div>

          <div className='card card-bg'>
            <p className='currentColor'>Remembers what user said earlier in the conversation</p>
          </div>

          <div className='card card-bg'>
            <p className='currentColor'>Allows user to provide follow-up corrections</p>
          </div>

          <div className='card card-bg'>
            <p className='currentColor'>Trained to decline inappropriate requests</p>
          </div>

        </div>

        <div className='inner'>
          <div className="card">
            <Warning />
            <h4 className="currentColor">Limitations</h4>
          </div>

          <div className='card card-bg'>
            <p className='currentColor'>May occasionally generate incorrect information</p>
          </div>

          {/* <div className='card card-bg'>
            <p className='currentColor'>May occasionally produce harmful instructions or biased content</p>
          </div>

          <div className='card card-bg'>
            <p className='currentColor'>Limited knowledge of world and events after 2021</p>
          </div> */}

        </div>
      </div>
      <div className={`collapsible-panel ${isPanelOpen ? 'open' : ''}`}>
        <button className="toggle-panel" onClick={() => setIsPanelOpen(!isPanelOpen)}>
          {isPanelOpen ? 'Close' : 'Open'}
        </button>
        {isPanelOpen && (
          <div className="panel-content">
            {transcribedText.map((text, index) => (
              <p key={index} className="chat-message">{text}</p>
            ))}
          </div>
        )}
      </div>
    </div>
  );
});

export default New;