import logo from './logo.svg';
import React from 'react';
import './App.css';
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import Login from './components/Login';
import Instruction from './components/Instruction';
import Calibration from './components/Calibration';
import Test from './components/Test';
import Report from './components/Report';

class App extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      msg:null,
      login:true,
      instructions:false,
      calibration:false,
      test:false,
      report:false
    }
    this.setMessage = this.setMessage.bind(this)
  }
  setMessage(msg){
    this.setState({msg:msg})
  }
  render(){
    return (
      <div className="App">
        {this.state.login?
         <Login setInstructions={(val)=>this.setState({instructions:val,login:false})}/>:this.state.instructions?
         <Instruction setCalibration={(val)=>this.setState({calibration:val,instructions:false})}/>:this.state.calibration?
         <Calibration setTest={(val)=>this.setState({test:val,calibration:false})}/>:this.state.test?
        <Test setReport={(val)=>this.setState({report:val,test:false})}/>:this.state.report?
        <Report/>:''
        }
        {/* <Message msg={this.state.msg} setMessage={this.setMessage}/>
        <Login setMessage={this.setMessage}/> */}
        {/* <Router> */}
         {/* <Login setMessage={this.setMessage}/>  */}
          {/* <Switch>
            <Route exact path="/" component={Login}/>
            <Route exact path="/instructions" component={Instruction} />
            <Route exact path="/calibration" component={Calibration} />
            <Route exact path="/test" component={Test} />
          </Switch>
        </Router> */}
      </div>
    );
  } 
}

export default App;
