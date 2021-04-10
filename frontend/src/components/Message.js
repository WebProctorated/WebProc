import React, { Component } from 'react'

export default class Message extends Component {
    constructor(props){
        super(props);
    }
    messageDisappear(){
        setTimeout(() => {
            this.props.setMessage(null)
        }, 3000);
    }
    render() {
        return this.props.msg && this.props.msg !== ''? (
            <div style={{backgroundColor:'yellow',padding:'2vh',borderWidth:'1px',borderRadius:'5px',borderColor:'black', display:'absolute',top:'2vh'}}>
                <h2>{this.props.msg}</h2>
                {/* {this.messageDisappear()} */}
            </div>
        ):''
    }
}
