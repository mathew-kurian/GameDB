import React from 'react'
import {Link} from 'react-router'

const App = React.createClass({
  getInitialState(){
    return {show: true}
  },
  hide(){
    this.setState({show: false});
  },
  render() {
    return (
      <div className={"full " + this.props.routes[this.props.routes.length - 1].rootClassName}>
        { this.state.show ? <div style={{border:'1px solid rgba(255, 255, 255, 0.22)',position:'fixed',bottom:20,right:20,maxWidth:400,borderRadius:5,background:'rgba(0, 0, 0, 0.58)',padding:10,zIndex:5,fontSize:11}}><b>Holaa</b><br/>Check out our HardCarry.me widget for <Link
          to={'/game/24024'} onClick={this.hide} style={{color:'white',fontWeight:'bold',textDecoration:'none'}}>League of Legend</Link></div>
        : null }
        {this.props.children}
      </div>
    )
  }
});

module.exports = App;