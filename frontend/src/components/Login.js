import React, { Component } from 'react';
import bgImage from '../assets/download.jpg';
import useHistory from 'react';
import { withAlert } from 'react-alert'

// const HistoryProvider = props =>{
//     const callHistory = () => {
//         let history = useHistory();
//         history.push('/instructions')
//         return  
//     }
//     return (<><div></div>{callHistory()}</>)
// }

class Login extends Component {
    constructor(props){
        super(props);
        console.log(props)
        this.state={
            enrollment:'',
            testId:'',
            history:props.history,
            HistoryProvider:false
        }
        this.onChange = this.onChange.bind(this);
        this.verifyStudent =this.verifyStudent.bind(this);
    }

    onChange(e){
        this.setState({[e.target.name]:e.target.value})
    }

    verifyStudent(){
        if(this.state.testId !== null && this.state.testId !== '' && this.state.enrollment !== null && this.state.enrollment !== ''){
            console.log(this.props)
            fetch('http://127.0.0.1:5000/login',{
                method:'POST',
                headers:{
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body:JSON.stringify({
                    enrollment:this.state.enrollment,
                    testId:this.state.testId
                })
            }).then(res=>{
                if(res.status === 201){
                    this.props.alert.show('Successfully Logged in !!');
                    console.log(this.props)
                    // this.setState({HistoryProvider:true})
                    this.props.setInstructions(true);
                    // this.props.history.push('/instructions')
                }
                else if(res.status === 400){
                    this.props.alert('Server Error, Login Again!!');
                }
                else if(res.status === 401){
                    this.props.alert('Invalid Login Credentials!!');
                }
                console.log(res);
            })
            .catch(err=>{
                console.log(err)
            })
        }
        
    }

    render() {
        return (
            <div style={{backgroundImage:`url(${bgImage})`, height:'100%'}}>
                {/* {this.state.HistoryProvider?this.props.histpry.push('/instructions'):''} */}
                <div className="container col-md-4 mx-auto" style={{height:'100%',display:'flex' }}>
                <div className="jumbotron" style={{ opacity: '0.95', backgroundColor:'#e3e5e6', padding:'0', margin:'auto'}}>
                    <div className="jumbotron-content" style={{padding:'2rem'}}>
                        <h1 style={{ fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif', textAlign: 'center' }}>
                            Login here</h1>
                        {/* <form> */}
                            <div className="form-row">
                                <div className="form-group col-md-12 mx-auto">
                                    <label htmlFor="inputEmail4">Enrollment Number</label>
                                    <input onChange={this.onChange} className="form-control" id="inputEmail4" placeholder="Enrollment No." name="enrollment" value={this.state.enrollment}/>
                                </div>
                                <div className="form-group col-md-12 mx-auto">
                                    <label htmlFor="inputPassword4">Test Id</label>
                                    <input onChange={this.onChange} type="password" className="form-control" id="inputPassword4" placeholder="Test Id" name="testId" value={this.state.testId}/>
                                </div>
                            </div>
                            <div style={{ textAlign: 'center' }}>
                                <button onClick={()=>this.verifyStudent()} className="btn btn-primary" id="loginbutton">Sign in</button>
                            </div>
                        {/* </form> */}
                    </div>
                </div>
             </div>
            </div>
        )
    }
}

export default withAlert()(Login);