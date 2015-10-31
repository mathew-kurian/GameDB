var React = require('react');
import { Link } from 'react-router'

var Header = React.createClass({
  getInitialState(){
    return {}
  },
  render(){
    return (
      <div style={{background:this.props.theme}}>
        <div className="container" style={{position:'relative'}}>
          <nav className="navbar">
            <ul className="nav navbar-nav">
              <li>
                <Link to="/">Home</Link>
              </li>
              <li>
                <Link className={this.props.mode === 'about' ? 'active nav-active' : null}
                      to="/about">About</Link>
              </li>
              <li>
                <Link className={this.props.mode === 'games' ? 'active nav-active' : null}
                      to="/games">Games</Link>
              </li>
              <li>
                <Link className={this.props.mode === 'platforms' ? 'active nav-active' : null}
                      to="/platforms">Platforms</Link>
              </li>
              <li>
                <Link className={this.props.mode === 'companies' ? 'active nav-active' : null}
                      to="/companies">Companies</Link>
              </li>
            </ul>
          </nav>
        </div>
        <div className='page-head' style={{background:'transparent'}}>
          <div className="container">
            <h1
              style={{fontSize:'41px',color:'#000',fontWeight:'bold',letterSpacing:'1px',textTransform:'uppercase'}}>{this.props.title}</h1>

            <h4
              style={{fontWeight:300,lineHeight: 1.4,color: 'rgba(0, 0, 0, 0.4)',fontSize: 24}}>The purpose of this
              project to is provide an interactive way to track the dependencies between video-games, platforms, and
              game companies.</h4>
          </div>
        </div>
      </div>
    )
  }
});

module.exports = Header;