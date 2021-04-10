import React, { Component } from 'react'

export default class Instruction extends Component {
    constructor(props){
        super(props);
        this.state={
            accepted:false
        }
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    handleSubmit(){
        if(this.state.accepted === true){
            window.location.href='/calibration';
        }
        else{
            alert('accept the instructions');
        }
    }
    render() {
        return (
            <div>
                <div div class="mx-auto" style={{width:'80%',height:'80%'}}>
                    <ul class="list-group">
                        <li class="list-group-item active" aria-current="true"><h1> Insturctions for Test paper</h1></li>
                        <li><h1>Student must be in the frame throughout the test. <br/>If he/she moves out, it will generate warning.</h1></li>
                        <li><h3>Test duration: 15 mins</h3></li>
                        <li><h3>Student should not switch tabs during examination.</h3></li>
                        <li><h3>Camera will be on during the test, if 3 warning are called, test will be terminated.</h3></li>
                        <li><h3>Every correct answer will award you 1 mark.</h3></li>
                        <li><h3>And incorrect will deduct .25 mark.</h3></li>
                        <li><h3>Test will have __ number of questions.</h3></li>
                        <li><h3>__ Maximum marks</h3></li>
                        <li><h3>During test proper internet collectivity must be maintained.</h3></li>
                        <li><h3>It will be MCQ test</h3></li>
                    </ul>
                    <input type="checkbox" class="form-check-input" id="exampleCheck1" onChange={()=>this.setState({accepted:true})} value={this.state.accepted}/>
                    <label class="form-check-label" for="exampleCheck1">Ready for exam ?</label>
                    <button class="btn btn-primary" onClick={()=>this.handleSubmit()}>Submit</button>
                </div>
            </div>
        )
    }
}
