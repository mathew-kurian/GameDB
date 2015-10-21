var React = require('react');
var _ = require('underscore');
var moment = require('moment');

var NOT_AVAILABLE = '';

var Header = React.createClass({
  getInitialState(){
    return {}
  },
  render(){
    var tbody;

    switch (this.props.mode) {
      case "games":
        tbody = (
          <tbody>
          <tr>
            <th scope="row">Genres</th>
            <td>{_.pluck(this.props.genres, 'name').join('; ') || NOT_AVAILABLE}</td>
          </tr>
          <tr>
            <th scope="row">Platforms</th>
            <td>{_.pluck(this.props.release_dates, 'platform_name').join('; ') || NOT_AVAILABLE}</td>
          </tr>
          <tr>
            <th scope="row">Themes</th>
            <td>{_.pluck(this.props.themes, 'name').join('; ') || NOT_AVAILABLE}</td>
          </tr>
          <tr>
            <th scope="row">Rating</th>
            <td>{Number(this.props.rating || this.props.rating || "Not available").toFixed(2)}</td>
          </tr>
          </tbody>
        );
        break;
      case "publishers":
        tbody = (
          <tbody>
          <tr>
            <th scope="row">Address</th>
            <td>{this.props.location_address || NOT_AVAILABLE}</td>
          </tr>
          <tr>
            <th scope="row">City</th>
            <td>{this.props.location_city || NOT_AVAILABLE}</td>
          </tr>
          <tr>
            <th scope="row">State</th>
            <td>{this.props.location_state || NOT_AVAILABLE}</td>
          </tr>
          <tr>
            <th scope="row">County</th>
            <td>{this.props.location_country || NOT_AVAILABLE}</td>
          </tr>
          <tr>
            <th scope="row">Founded</th>
            <td>{this.props.date_founded ? moment(this.props.date_founded).format('MMM YYYY') : NOT_AVAILABLE}</td>
          </tr>
          <tr>
            <th scope="row">Phone</th>
            <td>{this.props.phone || NOT_AVAILABLE}</td>
          </tr>
          <tr>
            <th scope="row">Website</th>
            <td>{this.props.website || NOT_AVAILABLE}</td>
          </tr>
          <tr>
            <th scope="row">Deck</th>
            <td>{this.props.deck}</td>
          </tr>
          </tbody>
        );
        break;
      case "platforms":
        tbody = (
          <tbody>
          <tr>
            <th scope="row">Company</th>
            <td>{this.props.company ? this.props.company.name : NOT_AVAILABLE}</td>
          </tr>
          <tr>
            <th scope="row">Price</th>
            <td>{this.props.original_price || NOT_AVAILABLE}</td>
          </tr>
          <tr>
            <th scope="row">Date</th>
            <td>{this.props.release_date ? moment(this.props.release_date).format('llll') : NOT_AVAILABLE}</td>
          </tr>
          <tr>
            <th scope="row">Deck</th>
            <td>{this.props.deck || NOT_AVAILABLE}</td>
          </tr>
          </tbody>
        );
        break;
    }

    return (
      <div style={{background:'rgba(0,0,0,0.4)',position:'relative'}}>
        <div className='blur'
             style={{width:'100%',height:'100%',top:0,left:0, backgroundImage: 'url(' + (this.props.company_logo ? "http://igdb.com/" +  this.props.company_logo.url : this.props.images[0]) + ')',backgroundPosition:'center center',backgroundRepeat:'no-repeat',backgroundSize:'cover',backgroundColor:'#555', position:'absolute',zIndex:-1}}/>
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
                <a className={this.props.mode === 'platforms' ? 'active nav-active' : null}
                   href="../platforms.html">Platforms</a>
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
                style={{width:'100%', display:'inline-block', height: 250, borderRadius: 5,backgroundImage: 'url(' + (this.props.company_logo ? "http://igdb.com/" +  this.props.company_logo.url : this.props.images[0]) + ')',backgroundPosition:'center center',backgroundRepeat:'no-repeat',backgroundSize:'cover',backgroundColor:'#888',verticalAlign:'top'}}
                className='img-rounded'/>
            </div>
            <div className="col-md-9">
              <h1
                style={{display:'inline-block',fontSize:'41px',color:'#FFF',fontWeight:'bold',letterSpacing:'1px',textTransform:'uppercase',verticalAlign:'top',marginTop:0}}>{this.props.name}</h1>
              <table className="compressed">
                { tbody }
              </table>
            </div>
          </div>
        </div>
      </div>
    )
  }
});

module.exports = Header;