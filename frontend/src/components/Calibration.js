import React, { Component } from 'react';
import { withAlert } from 'react-alert';
import { CountdownCircleTimer } from "react-countdown-circle-timer";

class Calibration extends Component {
    constructor(props){
        super(props);
        this.state={
            stream:undefined,
            socket:window.io.connect(window.location.protocol + '//' + document.domain + ':' + '5000' + "/test")
        }
        this.handleClick = this.handleClick.bind(this);
        this.sendSnapshot = this.sendSnapshot.bind(this)
    }

    componentDidMount(){
        this.state.socket.on('msg',(data)=>{
            console.log(data);
            if(data.error === true)
                this.props.alert.show('error: '+data.msg)
            else
                this.props.alert.show(data.msg)
        })
    }

    sendSnapshot(){
        let video = document.querySelector("#videoElement");
        let canvas = document.querySelector("#canvasElement");
        let ctx = canvas.getContext('2d');

        ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 300, 150);

        let dataURL = canvas.toDataURL('image/jpeg');
        this.state.socket.emit('input image', dataURL);

        this.state.socket.emit('output image')

        var img = new Image();
        this.state.socket.on('out-image-event', (data)=> {
            console.log(data)
        });
    }

    handleClick(){
        let video = document.querySelector("#videoElement");
        var localMediaStream = null;
        var constraints = {
            video: {
                width: { min: 640 },
                height: { min: 480 }
            }
        };
        this.state.socket.on('connect', ()=>{
            console.log('Connected!');
        });
        navigator.mediaDevices.getUserMedia(constraints).then((stream)=>{
            video.srcObject = stream;
            localMediaStream = stream;
            var self = this;
            // let sendSnapshot = this.sendSnapshot
            setInterval(()=>self.sendSnapshot(), 50);
        }).catch((error)=>{
            console.log(error);
        });

    }
    render() {
        const minuteSeconds = 60;
        const hourSeconds = 3600;
        const daySeconds = 86400;
        const timerProps = {
            isPlaying: true,
            size: 120,
            strokeWidth: 6
          };
          const renderTime = (dimension, time) => {
            return (
              <div className="time-wrapper">
                <div className="time">{time}</div>
                <div>{dimension}</div>
              </div>
            );
          };
          const getTimeSeconds = (time) => (minuteSeconds - time) | 0;
        return (
            <div>
                <CountdownCircleTimer
                    {...timerProps}
                    colors={[["#218380"]]}
                    duration={minuteSeconds}
                    initialRemainingTime={10 % minuteSeconds}
                    onComplete={(totalElapsedTime) => console.log('time up')}
                >
                    {({ elapsedTime }) =>
                    renderTime("seconds", getTimeSeconds(elapsedTime))
                    }
                </CountdownCircleTimer>
                <div><video autoPlay={true} id="videoElement" style={{display:'none'}}></video>
                <canvas id="canvasElement"></canvas></div>
                <button onClick={()=>this.handleClick()}>Start for Calibration</button>
            </div>
        )
    }
}

export default withAlert()(Calibration);