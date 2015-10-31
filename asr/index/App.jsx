var React = require('react');
var Parallax = require('react-parallax');
import {Link} from 'react-router'

var H = 30;

var App = React.createClass({
  getInitialState(){
    return {height: window.innerHeight - H};
  },
  _handleResize: function () {
    this.setState({height: window.innerHeight - H + 'px'});
  },
  componentDidMount: function () {
    window.onresize = this._handleResize;
  },
  render: function () {
    return (
      <div>
        <Parallax bgImage={"/assets/images/killzone-0.png"} strength={300}>
          <div style={{height:this.state.height}}>
            <div className='center-vertical' style={{paddingLeft:'50px',width:430}}>
              <div
                style={{background: '#ffc846', color: '#000', display: 'inline-block', padding: '2px 10px', fontSize: 12, textTransform: 'uppercase', letterSpacing: 1, fontWeight: 400, marginBottom: 10}}>
                introducing
              </div>
              <div
                style={{color: '#fff', fontSize: 41, width: 400, letterSpacing: 1, verticalAlign: 'top', textTransform: 'uppercase', lineHeight: '39px'}}>
                <b>4play.DB:</b> <br />A Game Database
              </div>
              <div
                style={{color: '#fff', fontSize: 14, opacity: '0.9', width: '100%', textTransform: 'none', fontWeight: 'normal', lineHeight: '18px', marginTop: 10, letterSpacing: 0}}
                className="subtitle">Easy to manage system allows you to search your favorite games and understand their
                relationships. We also offer a REST API for enabling developers.
              </div>
              <a
                style={{color: '#FFF', padding: '8px 12px', fontSize: 12, fontWeight: 400, border: '1px solid white', borderRadius: 5, textTransform: 'uppercase', display: 'inline-block', letterSpacing: 1, marginTop: 20, textDecoration: 'none'}}
                href='games.html'>start browsing
              </a>
            </div>
          </div>
        </Parallax>
        <Parallax bgImage={"/assets/images/utaustin-0.jpg"} strength={100}>
          <div style={{height:350,textAlign:"center"}}>
            <div className='center-vertical' style={{width:430,margin: "0 auto"}}>
              <div
                style={{background: '#ffc846', color: '#000', display: 'inline-block', padding: '2px 10px', fontSize: 12, textTransform: 'uppercase', letterSpacing: 1, fontWeight: 200, marginBottom: 10}}>
                built for
              </div>
              <div
                style={{color: '#fff', fontSize: 30, width: 400, letterSpacing: 1, verticalAlign: 'top', textTransform: 'uppercase', lineHeight: '29px'}}
                className="title"><b>Downing:</b> CS373
              </div>
              <div
                style={{color: '#fff', fontSize: 14, opacity: '0.9', width: '100%', textTransform: 'none', fontWeight: 'normal', lineHeight: '18px', marginTop: 10, letterSpacing: 0}}
                className="subtitle">Special thanks to IGDB, GiantBomb, and Google Images for providing the data. Hook
                em' horns
              </div>
            </div>
          </div>
        </Parallax>

        <div className="flex" style={{height:H,position:'fixed',bottom:0,left:0,right:0}}>
          <div className="box full">
            <Link to="/about"
                  style={{background: '#ffc846', color: '#000', display: 'inline-block', fontSize: 12, textTransform: 'uppercase', letterSpacing: 1, fontWeight: 400, lineHeight: H + 'px',borderRight:'1px solid #e4ae29', textDecoration:'none',textAlign:'center',width:'100%'}}>
              <b>About</b> Team
            </Link>
          </div>
          <div className="box full">
            <Link to="/games"
                  style={{background: '#ffc846', color: '#000', display: 'inline-block', fontSize: 12, textTransform: 'uppercase', letterSpacing: 1, fontWeight: 400, lineHeight: H + 'px',borderRight:'1px solid #e4ae29',textDecoration:'none', textAlign:'center',width:'100%'}}>
              <b>Games</b> Model
            </Link>
          </div>
          <div className="box full">
            <Link to="/platforms"
                  style={{background: '#ffc846', color: '#000', display: 'inline-block', fontSize: 12, textTransform: 'uppercase', letterSpacing: 1, fontWeight: 400, lineHeight: H + 'px',borderRight:'1px solid #e4ae29', textDecoration:'none',textAlign:'center',width:'100%'}}>
              <b>Platforms</b> Model
            </Link>
          </div>
          <div className="box full">
            <Link to="/companies"
                  style={{background: '#ffc846', color: '#000', display: 'inline-block', fontSize: 12, textTransform: 'uppercase', letterSpacing: 1, fontWeight: 400, lineHeight: H + 'px', textDecoration:'none',textAlign:'center',width:'100%'}}>
              <b>Publishers</b> Model
            </Link>
          </div>
        </div>
      </div>
    )
  }
});

module.exports = App;