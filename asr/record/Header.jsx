var React = require('react');
var _ = require('underscore');

var Header = React.createClass({
  getInitialState(){
    return {}
  },
  render(){
    return (
      <div style={{background:'rgba(0,0,0,0.5)',position:'relative'}}>
        <div className='blur'
             style={{width:'100%',height:'100%',top:0,left:0, backgroundImage: 'url(' + this.props.images[0] + ')',backgroundPosition:'center center',backgroundRepeat:'no-repeat',backgroundSize:'cover',backgroundColor:'#777', position:'absolute',zIndex:-1}}/>
        <div className="container" style={{position:'relative'}}>
          <nav className="navbar">
            <ul className="nav navbar-nav">
              <li>
                <a href="../index.html">Home</a>
              </li>
              <li>
                <a href="../about.html">About</a>
              </li>
              <li>
                <a className={this.props.mode === 'games' ? 'active nav-active' : null}
                   href="../games.html">Games</a>
              </li>
              <li>
                <a className={this.props.mode === 'releases' ? 'active nav-active' : null}
                   href="../releases.html">Releases</a>
              </li>
              <li>
                <a className={this.props.mode === 'publishers' ? 'active nav-active' : null}
                   href="../publishers.html">Publishers</a>
              </li>
            </ul>
          </nav>
        </div>
        <div className='page-head' style={{background:'transparent'}}>
          <div className="container">
            <div className='col-md-3'>
              <div
                style={{width:250, display:'inline-block', height: 250, borderRadius: 5,background: 'url(' + this.props.images[0] + ') center center no-repeat',backgroundSize:'cover',verticalAlign:'top'}}
                className='img-rounded'/>
            </div>
            <div className="col-md-9">
              <h1
                style={{display:'inline-block',fontSize:'41px',color:'#FFF',fontWeight:'bold',letterSpacing:'1px',textTransform:'uppercase',verticalAlign:'top'}}>{this.props.name}</h1>
              <table class="table table-striped" style={{width:'100%'}}>
                <tbody>
                <tr>
                  <th scope="row">Genres</th>
                  <td>{_.pluck(this.props.genres, 'name').join('; ')}</td>
                </tr>
                <tr>
                  <th scope="row">Platforms</th>
                  <td>{_.pluck(this.props.release_dates, 'platform_name').join('; ')}</td>
                </tr>
                <tr>
                  <th scope="row">Themes</th>
                  <td>{_.pluck(this.props.themes, 'name').join('; ')}</td>
                </tr>
                <tr>
                  <th scope="row">Rating</th>
                  <td>{this.props.rating || 4.1}</td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    )
  }
});

module.exports = Header;