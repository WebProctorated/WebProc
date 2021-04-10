import React, { Component } from 'react';
import { withAlert } from 'react-alert'

class Calibration extends Component {
    constructor(props){
        super(props);
        this.state={
            stream:undefined
        }
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(){

        fetch('http://127.0.0.1:5000/calibration',{
                method:'POST',
                headers:{
                    "Content-Type": "application/json"
                },
                body:JSON.stringify({
                    // authorization id
                })
            }).then(res=>{
                console.log(res)
                if(res.status === 404){
                    this.props.alert.show(res.statusText);
                    this.state.stream = undefined
                }
                else if( res.state === 201){
                    res.json().then(data=>this.setState({stream:data.body}))
                }
            }).catch(err=>{console.log(err)})
    }
    render() {
        return (
            <div>
                <div><img 
                // disabled={this.state.stream === undefined ? true : false} 
                src={this.state.stream} /></div>
                <button onClick={()=>this.handleClick()}>Start for Calibration</button>
            </div>
        )
    }
}

export default withAlert()(Calibration);