import React from 'react'

const Webcam = (prop: WebcamPropType) => {

    return (
        <>
            <div>
                <video style={{ margin: "auto", display: "block", height:"500px", width: "100%" }} playsInline loop muted autoPlay ref={prop.webcamRef} >
                    <source id="video-source" ref={prop.webCamSrcRef} />
                </video>
            </div>
        </>
    );
}
interface WebcamPropType {
    webcamRef: React.MutableRefObject<HTMLVideoElement | null>,
    webCamSrcRef: React.MutableRefObject<HTMLSourceElement | null>,
    isPreviewing: boolean,
    isRecording: boolean,
}

export default Webcam