var React = require('react');
var Parallax = require('react-parallax');

var App = React.createClass({
  getInitialState(){
    return {height: window.innerHeight};
  },
  _handleResize: function () {
    this.setState({height: window.innerHeight + 'px'});
  },
  componentDidMount: function () {
    window.onresize = this._handleResize;
  },
  render: function () {
    return (
      <div>
        <Parallax bgImage={$ASSETS + "images/killzone-0.png"} strength={300}>
          <div style={{height:this.state.height}}>
            <div className='center-vertical' style={{paddingLeft:'50px',width:430}}>
              <div
                style={{background: '#ffc846', color: '#000', display: 'inline-block', padding: '2px 10px', fontSize: 12, textTransform: 'uppercase', letterSpacing: 1, fontWeight: 200, marginBottom: 10}}>
                introducing
              </div>
              <div
                style={{color: '#fff', fontSize: 41, width: 400, letterSpacing: 1, verticalAlign: 'top', textTransform: 'uppercase', lineHeight: '39px'}}
                className="title"><b>4play.DB:</b> <br />A Game Database
              </div>
              <div
                style={{color: '#fff', fontSize: 14, opacity: '0.9', width: '100%', textTransform: 'none', fontWeight: 'normal', lineHeight: '18px', marginTop: 10, letterSpacing: 0}}
                className="subtitle">Easy to manage system allows you to search your favorite games and understand their
                relationships. We also offer a REST API for enabling developers.
              </div>
              <a
                style={{color: '#FFF', padding: '8px 12px', fontSize: 12, fontWeight: 'bold', border: '1px solid white', borderRadius: 5, textTransform: 'uppercase', display: 'inline-block', letterSpacing: 1, marginTop: 20, textDecoration: 'none'}}
                className="button" href='games.html'>start browsing
              </a>
            </div>
          </div>
        </Parallax>
        <Parallax bgImage={$ASSETS + "images/titanfall-0.png"} strength={100}>
          <div style={{height:this.state.height / 2}}>
            <div className='center-vertical' style={{paddingLeft:'50px',width:430}}>
              <div
                style={{background: '#ffc846', color: '#000', display: 'inline-block', padding: '2px 10px', fontSize: 12, textTransform: 'uppercase', letterSpacing: 1, fontWeight: 200, marginBottom: 10}}>
                introducing
              </div>
              <div
                style={{color: '#fff', fontSize: 41, width: 400, letterSpacing: 1, verticalAlign: 'top', textTransform: 'uppercase', lineHeight: '39px'}}
                className="title"><b>4play.DB:</b> <br />A Game Database
              </div>
              <div
                style={{color: '#fff', fontSize: 14, opacity: '0.9', width: '100%', textTransform: 'none', fontWeight: 'normal', lineHeight: '18px', marginTop: 10, letterSpacing: 0}}
                className="subtitle">Easy to manage system allows you to search your favorite games and understand their
                relationships. We also offer a REST API for enabling developers.
              </div>
              <a
                style={{color: '#FFF', padding: '8px 12px', fontSize: 12, fontWeight: 'bold', border: '1px solid white', borderRadius: 5, textTransform: 'uppercase', display: 'inline-block', letterSpacing: 1, marginTop: 20, textDecoration: 'none'}}
                className="button" href='games.html'>start browsing
              </a>
            </div>
          </div>
        </Parallax>
      </div>
    )
  }
});

module.exports = App;