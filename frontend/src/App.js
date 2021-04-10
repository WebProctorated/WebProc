import logo from './logo.svg';
import React from 'react';
import './App.css';
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import Login from './components/Login';
import Instruction from './components/Instruction';
import Calibration from './components/Calibration';
import Test from './components/Test';
import Message from './components/Message';

class App extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      msg:null
    }
    this.setMessage = this.setMessage.bind(this)
  }
  setMessage(msg){
    this.setState({msg:msg})
  }
  render(){
    return (
      <div className="App">
        {/* <Message msg={this.state.msg} setMessage={this.setMessage}/>
        <Login setMessage={this.setMessage}/> */}
        <Router>
          {/* <Login setMessage={this.setMessage}/> */}
          <Switch>
            <Route exact path="/" component={Login}/>
            <Route exact path="/instructions" component={Instruction} />
            <Route exact path="/calibration" component={Calibration} />
            <Route exact path="/test" component={Test} />
          </Switch>
        </Router>
      </div>
    );
  } 
}

export default App;
