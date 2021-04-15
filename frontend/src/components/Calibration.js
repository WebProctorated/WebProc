import React, { Component } from 'react';
import { withAlert } from 'react-alert';
import { CountdownCircleTimer } from "react-countdown-circle-timer";

class Calibration extends Component {
    constructor(props) {
        super(props);
        this.state = {
            stream: undefined,
            socket: null,
            isPlaying: false,
            key: 0,
            id:undefined
        }
        this.handleClick = this.handleClick.bind(this);
    }

    componentDidMount() {
        document.getElementById('photo').setAttribute('src',window.src);
       window.src = null;
       var id = setInterval(()=>{
            fetch('http://localhost:5000/msg')
            .then(res=>{
                return res.json();
            }).then(data=>{
                if(data !== '')
                    this.props.alert.show(data);
                if(data === 'All Is Fine!! Good to Go!')
                    this.props.setTest(true);
            });
        },500
        )
        this.setState({id:id});
    }

    componentWillUnmount(){
        if(this.state.id)
            clearInterval(this.state.id);
    }

    handleClick() {
       fetch('http://localhost:5000/start_cal')
       .then(res=>{
           this.setState({isPlaying:true})
       })
       .catch(err=>console.log(err))
    }
    render() {
        const minuteSeconds = 60;
        const timerProps = {
            size: 120,
            strokeWidth: 6
        };
        const renderTime = (dimension, time) => {
            return (
                <div className="time-wrapper">
                    <div className="time" style={{ textAlign: 'center' }}>{time}</div>
                    <div>{dimension}</div>
                </div>
            );
        };
        const getTimeSeconds = (time) => (10 - time) | 0;
        return (
            <div>
                <div style={{ width: 'fit-content', position: 'absolute', top: '16vh', right: '3vw' }}>
                    <CountdownCircleTimer
                        {...timerProps}
                        isPlaying={this.state.isPlaying}
                        key={this.state.isPlaying}
                        colors={[["#218380"]]}
                        duration={10}
                        initialRemainingTime={this.state.isPlaying === false ? 10 : 10}
                        onComplete={(totalElapsedTime) => { console.log('time up'); this.setState({ isPlaying: false }) }}
                    >
                        {({ elapsedTime }) =>
                            renderTime("seconds", getTimeSeconds(elapsedTime))
                        }
                    </CountdownCircleTimer>
                </div>
                <div><video autoPlay={true} id="videoElement"
                    style={{ display: 'none' }}
                ></video>
                    <img id="photo" style={{ borderRadius: '5px', height: '70vh', width: '70vw', margin: '5vh 15vw' }} /></div>
                <div style={{ margin: 'auto', width: '25vw', display: 'flex', justifyContent: 'space-between' }}>
                    <button type="button" className="btn btn-info" onClick={() => this.handleClick()}>Start for Calibration</button>
                </div>
            </div>
        )
    }
}

export default withAlert()(Calibration);