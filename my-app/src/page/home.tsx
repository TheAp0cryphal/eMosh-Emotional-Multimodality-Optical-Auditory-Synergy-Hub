import React, { useEffect, useRef, useState } from 'react'
import Webcam from "../components/webcam"

import Plot from 'react-plotly.js';
import { Button, Typography } from '@mui/material';
import axios, { AxiosResponse } from 'axios';

const Home = () => {

    const [valence, setValence] = useState<Plotly.Datum>(0);
    const [arousal, setArousal] = useState<Plotly.Datum>(0);
    const [emoji, setEmoji] = useState<number>(0x1F928	);
    const [isPreviewing, setIsPreviewing] = useState(false);
    const [isRecording, setisRecording] = useState(false);


    const videoRef = useRef<HTMLVideoElement | null>(null);
    const videoSrcRef = useRef<HTMLSourceElement | null>(null);
    const currentStream = useRef<MediaStream | null>(null)
    const selectedFile = useRef<File>();
    const recordedMovie = useRef<Blob>();
    const mediaRecorderRef = useRef<MediaRecorder>();



    useEffect(() => {

        navigator.mediaDevices.getUserMedia({video: true, audio: true})
            .then((stream) => {
                if (videoRef.current) {
                    videoRef.current.srcObject = stream;
                }
                currentStream.current = stream;
            });

        return () => { }
    }, []);

    const updateTheta = (newTheta: Plotly.Datum) => {
        setValence(newTheta);
    }

    const sendFileForEmoji = (event: React.ChangeEvent<HTMLInputElement>) => {

        if (!event.target.files) return;

        console.log('Sending request for emoji');

        const data = new FormData();
        data.append("video", event.target!.files[0]);

        return axios.post('http://localhost:5000/upload_video', data)
            .then((response) => {
                onPostEmojiPrediction(response);
            });
    }

    const requestEmoji = () => {

        if (recordedMovie.current == undefined && selectedFile == null) {
            return;
        }

        console.log('Sending request for emoji');

        const data = new FormData();

        let movieFile: File;
        
        if (selectedFile.current) {
            movieFile = selectedFile.current;
        } else {
            movieFile = new File([recordedMovie.current!], `newWeb.webm`)
        }

        data.append("video", movieFile);

        return axios.post('http://localhost:5000/upload_video', data)
            .then((response) => {
                console.log(response.data);
                onPostEmojiPrediction(response);
            });
    }

    const onPostEmojiPrediction = (response: AxiosResponse<any, any>) => {
        console.log(response.data);

        console.log(response.data[0]);
        console.log(response.data[1]);

        const coords: number[] = response.data[0];

        const valence = coords[0];
        const arousal = coords[1];
        const emoji = response.data[1]

        setEmoji(Number(emoji))
        setValence(valence);
        setArousal(arousal);
    }

    const clearUpMovie = () => {
        if (videoRef.current) {
            videoRef.current.srcObject = null;
            videoRef.current.removeAttribute('src');
        }
        if (videoSrcRef.current) {
            videoSrcRef.current.src = '';
            console.log(videoSrcRef.current.src);
        }

    }

    const uploadLocalMovie = (file: File) => {
        if (!file) return;

        console.log(file.name);


        clearUpMovie();
        recordedMovie.current = undefined;
        selectedFile.current = file;

        console.log(selectedFile.current);


        const fileReader = new FileReader();

        fileReader.onload = (event) => {
            if (videoSrcRef.current != null) {
                console.log('fileReader.onload called');
                videoSrcRef.current.src = event.target!.result as string;
                console.log(videoSrcRef.current.src);

                videoRef.current!.load();

                setIsPreviewing(true);
            } else {
                console.log('videoSrcRef.current is null');
            }
        }

        fileReader.readAsDataURL(file);
    }

    const startRecording = async () => {

        console.log('recording started')

        recordedMovie.current = undefined;
        selectedFile.current = undefined;

        if (isPreviewing) {
            console.log('prop.isFileStreaming is true or recorded movie exists');

            setIsPreviewing(false);

            clearUpMovie();
            videoRef.current!.load();

            // wait for video stream from user camera
            const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
            console.log(stream);

            currentStream.current = stream;
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
            }
            videoRef.current?.load();
        }

        if (currentStream.current) {

            let recordedChunks: Blob[] = [];

            var options = {
                audioBitsPerSecond: 128000,
                videoBitsPerSecond: 2500000,
                mimeType: 'video/webm'
            }

            mediaRecorderRef.current = new MediaRecorder(currentStream.current, options);

            mediaRecorderRef.current.ondataavailable = event => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            }

            mediaRecorderRef.current.onstop = event => {

                const blob = new Blob(recordedChunks, {
                    type: 'video/webm'
                });

                recordedMovie.current = blob;

                console.log(recordedMovie.current);

                const outputUrl = URL.createObjectURL(blob);

                clearUpMovie();
                videoRef.current!.src = outputUrl;
                videoRef.current!.load();

                setIsPreviewing(true);
                // videoRef.current!.setAttribute("src", outputUrl);

                // clearUpMovie();
                // if(videoRef.current) {
                //     // prop.videoRef.current.src = outputUrl;
                //     videoRef.current.load();
                // }

                // let recordName = prompt('Please enter the name of your recording. Otherwise, the name will be a current time.');

                // if (!recordName) {
                //     recordName = new Date().toUTCString();
                // }

                // const link = document.createElement('a');
                // link.href = outputUrl;
                // link.download = recordName;
                // link.click();

            }

            mediaRecorderRef.current.start();
            setisRecording(true);
        }
    }

    const stopRecording = () => {
        console.log("recording stopped");

        if (mediaRecorderRef.current) {
            mediaRecorderRef.current.stop();
            mediaRecorderRef.current = undefined;

            setisRecording(false);
        }

    }

    return (
        <div style={{ display: 'flex', flexDirection: 'row', flex: '1', backgroundColor: "#EDF0F6", padding: "2%"}}>
            <div style={{ width: "50%" }}>
                <Typography variant="h5" align="center" fontWeight="600">
                    {
                        isPreviewing ? "Previewing" : isRecording ? "Recording" : "Record or upload  to predict Emoji!"
                    }
                </Typography>
                <Webcam
                    webcamRef={videoRef}
                    webCamSrcRef={videoSrcRef}
                    isPreviewing={isPreviewing}
                    isRecording={isRecording} />

                <Button style={buttonStyle1} variant="contained" onClick={isRecording ? stopRecording : startRecording}>
                    {
                        isRecording ? "Stop Recording" : "start Recording"
                    }
                </Button>

                <label style={{ margin: "1rem auto" }} htmlFor="upload-photo">
                    <input
                        style={{ display: 'block', margin: "auto" }}
                        id="upload-photo"
                        name="upload-photo"
                        type="file"
                        disabled={isRecording}
                        onChange={(event) => {
                            if (event.target.files != null && event.target.files.length > 0) {
                                uploadLocalMovie(event.target.files[0]);
                            }
                        }}
                    />

                    {/* <Button style={buttonStyle} variant="contained">
                        Upload button
                    </Button> */}
                </label>

                <Button style={buttonStyle2} variant="contained" onClick={requestEmoji}>
                    Predict emoji from your recorded/selected movie!
                </Button>
            </div>
            <div style={{ width: "50%", display: 'flex', flexDirection: 'column', alignItems: "center" }}>
                <Plot
                    data={[
                        {
                            x: [valence],
                            y: [arousal],
                            mode: 'markers',
                            type: 'scatter',
                            showlegend: false,
                            showscale: false,
                        }
                    ]}
                    layout={{
                        width: 500, height: 500, 
                        title: 'Circumplex Model',
                        xaxis: {
                            range: [-1, 1]
                        },
                        yaxis: {
                            range: [-1, 1]
                        },
                        
                    }}
                    style={{ 
                        // display: "block", 
                        // margin: "auto"
                    }}
                />
                <Typography style={{ margin: "5% 0 0 0 " }} variant="h5" align="center" fontWeight="600">Predicted Emoji</Typography>
                <div style={{height: "150px", width: '150px', backgroundColor: "#D9DFEF", display: "flex", alignItems: "center"}}>
                    <Typography style={{ margin: "auto" }} variant="h1" align="center" fontWeight="600">{String.fromCodePoint(emoji)}</Typography>
                </div>
                {/* <Button variant="contained" onClick={() => updateTheta(Math.random())}>
                    Change Point
                </Button> */}
            </div>
        </div>

    )
}

const buttonStyle1 = {
    margin: '1rem auto',
    display: "block",
    backgroundColor: "#5865F2"
}

const buttonStyle2 = {
    margin: '1rem auto',
    display: "block",
    backgroundColor: "#404EED"
}

export default Home