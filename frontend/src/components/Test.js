import React, { Component } from 'react';
import { withAlert } from 'react-alert';
import { CountdownCircleTimer } from "react-countdown-circle-timer";

class Test extends Component {
    constructor(props){
        super(props);
        this.state={
            stream:undefined,
            socket:null
        }
        this.startTest = this.startTest.bind(this);
        this.sendSnapshot = this.sendSnapshot.bind(this);
    }

    componentDidMount(){
        //js to restrict user to open only one tab.
        document.addEventListener('visibilitychange', ()=>{
          document.title = document.visibilityState;
          if(document.visibilityState == "hidden"){
            //show alert message
            window.alert("don't switch the tab, it will treated as cheating behaviour\n ");
            window.CHEAT = true;
            console.log(document.visibilityState);}
          });
          window.addEventListener('resize',(e)=>{
            window.alert("don't minimize the window, it will treated as cheating behaviour\n ");
            window.CHEAT = true;
            console.log('resize: ',e)
          })
          this.startTest()
      }

    sendSnapshot(){
        let video = document.querySelector("#videoElement");
        let canvas = document.querySelector("#canvasElement");
        let ctx = canvas.getContext('2d');

        ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 300, 150);

        let dataURL = canvas.toDataURL('image/jpeg');
        if(this.state.socket !== null){
            this.state.socket.emit('proctor', dataURL);
            this.state.socket.on('out-image-event', (data)=> {
                console.log(data)
            });
        }
        if(window.CHEAT === true){
            fetch('http://localhost:5000/cheat',{
                method:'POST',
                headers:{
                    'Content-Type': 'application/json',
                    'Accept':'application/json'
                },
                body:JSON.stringify({CHEAT:true})
            })
            window.CHEAT = false;
        }
    }

    startTest(){
        if(this.state.socket === null){
            this.state.socket = window.io.connect( window.location.protocol + '//' + document.domain + ':' + '5000' + "/test", {
            reconnection: true,
            reconnectionDelay: 1000,
            reconnectionDelayMax : 5000,
            reconnectionAttempts: Infinity})
        }

        console.log(this.state.socket)
        let video = document.querySelector("#videoElement");
        var localMediaStream = null;
        var constraints = {
            video: {
                width: { max: 640 },
                height: { max: 480 }
            }
        };
        navigator.mediaDevices.getUserMedia(constraints).then((stream)=>{
            video.srcObject = stream;
            localMediaStream = stream;
            var self = this;
            // let sendSnapshot = this.sendSnapshot
            let id = setInterval(()=>{
                if(this.state.socket === null)
                    clearInterval(id);
                self.sendSnapshot();
            }, 1000/16);
        }).catch((error)=>{
            console.log(error);
        });

        this.state.socket.on('msg',(data)=>{
            console.log(data);
            if(data.error === true)
            {
                // setMessage('error: '+data.msg,this.props.alert);
                this.props.alert.removeAll();
                this.props.alert.show('error: '+data.msg)
            }
            else
            {
                // setMessage(data.msg,this.props.alert);
                this.props.alert.removeAll();
                this.props.alert.show(data.msg)
            }
        })
        this.state.socket.on('connect',()=>console.log('connected'))
        this.state.socket.on('disconnect', ()=> {
            console.log('disconnected')
            this.state.socket.destroy();
            delete this.state.socket;
            this.state.socket = null;
            } );

    }
    render() {
        const minuteSeconds = 60;
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
          const getTimeSeconds = (time) => (10 - time) | 0;
        return (
            <div>
                <CountdownCircleTimer
                    {...timerProps}
                    colors={[["#218380"]]}
                    duration={9}
                    initialRemainingTime={10}
                    onComplete={(totalElapsedTime) => console.log('time up')}
                >
                    {({ elapsedTime }) =>
                    renderTime("seconds", getTimeSeconds(elapsedTime))
                    }
                </CountdownCircleTimer>
                <div><video autoPlay={true} id="videoElement" 
                style={{display:'none'}}
                ></video>
                <canvas id="canvasElement"></canvas></div>
                <button onClick={()=>this.handleClick()}>Submit Test</button>
            </div>
        )
    }
}

export default withAlert()(Test);