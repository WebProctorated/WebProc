import React, { Component } from 'react'

export default class Report extends Component {
    constructor(props){
        super(props);
        this.state = {
            cheatCount:0
        }
    }
    componentDidMount(){
        fetch('http://localhost:5000/getCheatCount')
        .then(res=>res.json())
        .then(data=>this.setState({cheatCount:data.count}));
    }
    render() {
        return (
            <div style={{display:'flex',margin:'auto',width:'fit-content',flexDirection:'column'}}>
                <img src="/plot.png"/>
                <div style={{paddingTop:'20px'}}>Cheating Count Detected: {this.state.cheatCount}</div>
            </div>
        )
    }
}
