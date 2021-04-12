import React, { Component } from 'react';
import { withAlert } from 'react-alert';
import { CountdownCircleTimer } from "react-countdown-circle-timer";

class Calibration extends Component {
    constructor(props){
        super(props);
        this.state={
            stream:undefined,
            socket:null,
            isPlaying:false,
            key:0
        }
        this.handleClick = this.handleClick.bind(this);
        this.sendSnapshot = this.sendSnapshot.bind(this);
    }

    componentDidMount(){
        this.setState({socket:window.io.connect(window.location.protocol + '//' + document.domain + ':' + '5000' + "/test")});
    }

    sendSnapshot(){
        // let video = document.querySelector("#videoElement");
        // let canvas = document.querySelector("#canvasElement");
        // let ctx = canvas.getContext('2d');

        // ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 300, 150);

        // let dataURL = canvas.toDataURL('image/jpeg');
        if(this.state.socket !== null){
            this.state.socket.emit('calibrate',{});

            // this.state.socket.emit('output image')
            fetch('http://localhost:5000/calibration',{
                method:'GET',
                headers:{'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8'}
            }).then(data=>{
                console.log(data)
                var photo = document.getElementById('photo')
                photo.setAttribute('src',data.body)
                // return data.body.text()
            })
            // .then(res=>console.log(res))
            this.state.socket.on('out-image-event', (data)=> {
                this.setState({isPlaying:true})
                this.setState({key:this.state.key+1})
                // console.log(data)
            });
        }
    }

    handleClick(){
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
        var self = this;
        let sendSnapshot = this.sendSnapshot
        let id = setInterval(()=>{
            if(this.state.socket === null)
                clearInterval(id);
            self.sendSnapshot();
        }, 1000/30);
        navigator.mediaDevices.getUserMedia(constraints).then((stream)=>{
            // video.srcObject = stream;
            // localMediaStream = stream;
            
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
            if(this.state.socket !== null){
                this.state.socket.destroy();
                delete this.state.socket;
                this.setState({socket:null})
            }
            } );

    }
    render() {
        const minuteSeconds = 60;
        const timerProps = {
            isPlaying: this.state.isPlaying,
            size: 120,
            strokeWidth: 6
          };
          const renderTime = (dimension, time) => {
            return (
              <div className="time-wrapper">
                <div className="time" style={{textAlign:'center'}}>{time}</div>
                <div>{dimension}</div>
              </div>
            );
          };
          const getTimeSeconds = (time) => (10 - time) | 0;
        return (
            <div>
                <div style={{ width: 'fit-content',position: 'absolute',top: '16vh', right: '3vw'}}>
                    <CountdownCircleTimer
                        {...timerProps}
                        key={this.state.key}
                        colors={[["#218380"]]}
                        duration={10}
                        initialRemainingTime={this.state.isPlaying === false?10:10}
                        onComplete={(totalElapsedTime) => {console.log('time up');this.setState({isPlaying:false})}}
                    >
                        {({ elapsedTime }) =>
                        renderTime("seconds", getTimeSeconds(elapsedTime))
                        }
                    </CountdownCircleTimer>
                </div>
                <div><video autoPlay={true} id="videoElement" 
                style={{display:'none'}}
                ></video>
                <img id="photo" style="-webkit-user-select: none;" src='blob:http://localhost:5000/calibration' style={{borderRadius: '5px',height: '70vh',width: '70vw',margin: '5vh 15vw'}}/></div>
                <div style={{ margin: 'auto',width: '25vw',display: 'flex',justifyContent: 'space-between'}}>
                    <button type="button" className="btn btn-info" onClick={()=>this.handleClick()}>Start for Calibration</button>
                    <button type="button" className="btn btn-success" onClick={()=>{window.location.href="/test"}}>Take Test</button>
                </div>
            </div>
        )
    }
}

export default withAlert()(Calibration);