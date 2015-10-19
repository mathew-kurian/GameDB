var React = require('react');

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
                <a href="index.html">Home</a>
              </li>
              <li>
                <a href="about.html">About</a>
              </li>
              <li>
                <a className={this.props.mode === 'games' ? 'active nav-active' : null}
                   href="games.html">Games</a>
              </li>
              <li>
                <a className={this.props.mode === 'releases' ? 'active nav-active' : null}
                   href="releases.html">Releases</a>
              </li>
              <li>
                <a className={this.props.mode === 'publishers' ? 'active nav-active' : null}
                   href="publishers.html">Publishers</a>
              </li>
            </ul>
          </nav>
        </div>
        <div className='page-head' style={{background:'transparent'}}>
          <div className="container">
            <h1
              style={{fontSize:'41px',color:'#000',fontWeight:'bold',letterSpacing:'1px',textTransform:'uppercase'}}>{this.props.title}</h1>

            <h4
              style={{fontWeight:300,lineHeight: 1.4,color: 'rgba(0, 0, 0, 0.4)',fontSize: 24}}>{this.props.description}</h4>
          </div>
        </div>
      </div>
    )
  }
});

module.exports = Header;