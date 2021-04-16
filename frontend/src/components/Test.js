import React, { Component } from 'react';
import { withAlert } from 'react-alert';
import { CountdownCircleTimer } from "react-countdown-circle-timer";

function watchVisibility(){
    document.title = document.visibilityState;
    if(document.visibilityState == "hidden"){
    //show alert message
    window.alert("don't switch the tab, it will treated as cheating behaviour\n ");
    window.CHEAT = true;
    console.log(document.visibilityState);}
}

function windowSizeChange(e){
    window.alert("don't minimize the window, it will treated as cheating behaviour\n ");
    window.CHEAT = true;
    console.log('resize: ',e)
}

class Test extends Component {
    constructor(props){
        super(props);
        this.state={
            stream:undefined,
            socket:null,
            isPlaying:false,
            id:undefined
        }
        this.startTest = this.startTest.bind(this);
        this.handleClick = this.handleClick.bind(this);
    }

    componentDidMount(){
        //js to restrict user to open only one tab.
        document.addEventListener('visibilitychange', watchVisibility);
        window.addEventListener('resize',windowSizeChange);
        this.startTest();
      }

    componentWillUnmount(){
        if(this.state.id)
            clearInterval(this.state.id);
        document.removeEventListener('visibilitychange',watchVisibility);
        window.removeEventListener('resize',windowSizeChange);
    }

    startTest(){
        document.getElementById('test_window').setAttribute('src',window.test_src);
        window.test_src=null;
        this.setState({isPlaying:true});
        var id = setInterval(()=>{
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
            fetch('http://localhost:5000/msg')
            .then(res=>{
                return res.json();
            }).then(data=>{
                if(data !== '')
                    this.props.alert.show(data);
                if(data === 'Test Done!!')
                    this.props.setReport(true);
            });
        },2000
        )

        this.setState({id:id});

    }
    handleClick(){
        fetch('http://localhost:5000/stop_test')
        .catch(err=>console.log(err))
    }
    render() {
        const timerProps = {
            isPlaying: true,
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
          const getTimeSeconds = (time) => (2 + (time % 60) / 60) | 0;
        return (
            <div>
                <div style={{ width: 'fit-content',position: 'absolute',top: '40vh', right: '10vw'}}>
                    <CountdownCircleTimer
                        {...timerProps}
                        isPlaying={this.state.isPlaying}
                        key={this.state.isPlaying}
                        colors={[["#218380"]]}
                        duration={2*60}
                        initialRemainingTime={this.state.isPlaying === false ? 2*60 : 2*60}
                        onComplete={(totalElapsedTime) => { console.log('time up'); this.setState({ isPlaying: false }) }}
                    >
                        {({ elapsedTime }) =>
                            renderTime("minutes", getTimeSeconds(elapsedTime))
                        }
                    </CountdownCircleTimer>
                </div>
                <div><video autoPlay={true} id="videoElement" 
                style={{display:'none'}}
                ></video>
                <img id="test_window" style={{backgroundColor: 'grey',borderRadius: '5px',height: '30vh',width: '25vw',marginLeft: '72vw',marginTop: '4vh'}}/></div>
                <div style={{width: 'fit-content',margin: 'auto',marginTop: '-30vh'}}>
                    <h1>7 Wonders of the World</h1>
                    <form action="" id="quiz" method="POST">
                        <ol>
                        
                            <li>Where is <u>Petra</u> located?</li>
                            
                                {/* <!-- <input type='radio' value='Jerash' name='Petra' />Jerash  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Jerash" name="Petra" id="flexRadioDefault1"/>Jerash
                                </div>
                            
                                {/* <!-- <input type='radio' value='Zarqa' name='Petra' />Zarqa  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Zarqa" name="Petra" id="flexRadioDefault1"/>Zarqa
                                </div>
                            
                                {/* <!-- <input type='radio' value='Ma&#39;an Governorate' name='Petra' />Ma&#39;an Governorate  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Ma'an Governorate" name="Petra" id="flexRadioDefault1"/>Ma'an Governorate
                                </div>
                            
                                {/* <!-- <input type='radio' value='Amman' name='Petra' />Amman  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Amman" name="Petra" id="flexRadioDefault1"/>Amman
                                </div>
                            
                        
                            <li>Where is <u>Colosseum</u> located?</li>
                            
                                {/* <!-- <input type='radio' value='Bologna' name='Colosseum' />Bologna  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Bologna" name="Colosseum" id="flexRadioDefault1"/>Bologna
                                </div>
                            
                                {/* <!-- <input type='radio' value='Milan' name='Colosseum' />Milan  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Milan" name="Colosseum" id="flexRadioDefault1"/>Milan
                                </div>
                            
                                {/* <!-- <input type='radio' value='Rome' name='Colosseum' />Rome  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Rome" name="Colosseum" id="flexRadioDefault1"/>Rome
                                </div>
                            
                                {/* <!-- <input type='radio' value='Bari' name='Colosseum' />Bari  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Bari" name="Colosseum" id="flexRadioDefault1"/>Bari
                                </div>
                            
                        
                            <li>Where is <u>Great Wall of China</u> located?</li>
                            
                                {/* <!-- <input type='radio' value='China' name='Great Wall of China' />China  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="China" name="Great Wall of China" id="flexRadioDefault1"/>China
                                </div>
                            
                                {/* <!-- <input type='radio' value='Beijing' name='Great Wall of China' />Beijing  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Beijing" name="Great Wall of China" id="flexRadioDefault1"/>Beijing
                                </div>
                            
                                {/* <!-- <input type='radio' value='Shanghai' name='Great Wall of China' />Shanghai  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Shanghai" name="Great Wall of China" id="flexRadioDefault1"/>Shanghai
                                </div>
                            
                                {/* <!-- <input type='radio' value='Tianjin' name='Great Wall of China' />Tianjin  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Tianjin" name="Great Wall of China" id="flexRadioDefault1"/>Tianjin
                                </div>
                            
                        
                            <li>Where is <u>Taj Mahal</u> located?</li>
                            
                                {/* <!-- <input type='radio' value='Mumbai' name='Taj Mahal' />Mumbai  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Mumbai" name="Taj Mahal" id="flexRadioDefault1"/>Mumbai
                                </div>
                            
                                {/* <!-- <input type='radio' value='Agra' name='Taj Mahal' />Agra  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Agra" name="Taj Mahal" id="flexRadioDefault1"/>Agra
                                </div>
                            
                                {/* <!-- <input type='radio' value='New Delhi' name='Taj Mahal' />New Delhi  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="New Delhi" name="Taj Mahal" id="flexRadioDefault1"/>New Delhi
                                </div>
                            
                                {/* <!-- <input type='radio' value='Chennai' name='Taj Mahal' />Chennai  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Chennai" name="Taj Mahal" id="flexRadioDefault1"/>Chennai
                                </div>
                            
                        
                            <li>Where is <u>Egypt Pyramids</u> located?</li>
                            
                                {/* <!-- <input type='radio' value='Suez' name='Egypt Pyramids' />Suez  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Suez" name="Egypt Pyramids" id="flexRadioDefault1"/>Suez
                                </div>
                            
                                {/* <!-- <input type='radio' value='Tanta' name='Egypt Pyramids' />Tanta  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Tanta" name="Egypt Pyramids" id="flexRadioDefault1"/>Tanta
                                </div>
                            
                                {/* <!-- <input type='radio' value='Luxor' name='Egypt Pyramids' />Luxor  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Luxor" name="Egypt Pyramids" id="flexRadioDefault1"/>Luxor
                                </div>
                            
                                {/* <!-- <input type='radio' value='Giza' name='Egypt Pyramids' />Giza  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Giza" name="Egypt Pyramids" id="flexRadioDefault1"/>Giza
                                </div>
                            
                        
                            <li>Where is <u>Christ the Redeemer</u> located?</li>
                            
                                {/* <!-- <input type='radio' value='Olinda' name='Christ the Redeemer' />Olinda  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Olinda" name="Christ the Redeemer" id="flexRadioDefault1"/>Olinda
                                </div>
                            
                                {/* <!-- <input type='radio' value='Natal' name='Christ the Redeemer' />Natal  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Natal" name="Christ the Redeemer" id="flexRadioDefault1"/>Natal
                                </div>
                            
                                {/* <!-- <input type='radio' value='Rio de Janeiro' name='Christ the Redeemer' />Rio de Janeiro  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Rio de Janeiro" name="Christ the Redeemer" id="flexRadioDefault1"/>Rio de Janeiro
                                </div>
                            
                                {/* <!-- <input type='radio' value='Betim' name='Christ the Redeemer' />Betim  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Betim" name="Christ the Redeemer" id="flexRadioDefault1"/>Betim
                                </div>
                            
                        
                            <li>Where is <u>Machu Picchu</u> located?</li>
                            
                                {/* <!-- <input type='radio' value='Lima' name='Machu Picchu' />Lima  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Lima" name="Machu Picchu" id="flexRadioDefault1"/>Lima
                                </div>
                            
                                {/* <!-- <input type='radio' value='Piura' name='Machu Picchu' />Piura  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Piura" name="Machu Picchu" id="flexRadioDefault1"/>Piura
                                </div>
                            
                                {/* <!-- <input type='radio' value='Tacna' name='Machu Picchu' />Tacna  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Tacna" name="Machu Picchu" id="flexRadioDefault1"/>Tacna
                                </div>
                            
                                {/* <!-- <input type='radio' value='Cuzco Region' name='Machu Picchu' />Cuzco Region  --> */}
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" value="Cuzco Region" name="Machu Picchu" id="flexRadioDefault1"/>Cuzco Region
                                </div>
                            
                        
                        </ol>
                    </form>
                    </div>
                <button type="button" style={{margin: 'auto',display: 'block', marginBottom:'2vh'}} className="btn btn-success" onClick={()=>this.handleClick()}>Submit Test</button>
            </div>
        )
    }
}

export default withAlert()(Test);