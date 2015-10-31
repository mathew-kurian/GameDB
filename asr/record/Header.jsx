var React = require('react');
var _ = require('underscore');
var moment = require('moment');
import { Link } from 'react-router'
import history from '../History'
var Select = require('react-select');
var request = require('superagent');


var SPINNER = '/assets/dist/images/spinner-0.gif';

var Item = React.createClass({
  getInitialState(){
    return {}
  },
  componentWillUnmount: function () {
    if (this.req) {
      this.req.abort();
    }
  },
  componentWillReceiveProps(nextProps){
    if (this.req) {
      this.req.abort();
    }

    this.setState({image: SPINNER});
    this._fetch(nextProps);
  },
  _fetch: function (props) {
    var opath = props.path;
    var self = this;

    this.req = request.get('/api/' + opath + '/' + props[opath + '_id'])
      .end(function (err, res) {
        if (err || res.status !== 200) return self.req = null;
        try {
          self.setState({image: res.body.results[0].images[0].source});
        } catch (e) {
          // ignore
        }
      });
  },
  componentDidMount: function () {
    this._fetch(this.props);
  },
  render(){
    var opath = this.props.path;
    return (
      <div className='flex full'>
        <div className='box' style={{ borderRadius: 3, display: 'inline-block', marginRight: 10, position: 'relative',
                    top: -2, verticalAlign: 'middle',backgroundImage:"url('" + (this.state.image || SPINNER) + "')",
                    backgroundSize:'cover', height:40, width: 30, maxWidth: 30, minWidth: 30, marginRight:10}}/>
        <div className='box full'>
          {this.props[opath + '_name']}
          <div
            style={{letterSpacing:0,fontSize:12,textTransform:'none',opacity:0.5}}>{this.props[opath + '_deck']}</div>
        </div>
      </div>
    )
  }
});

var Tags = function (item) {
  return item.split(';').map(function (col, i) {
    return (<div className="columns" key={i}>{col}</div>)
  });
};

var DateForm = function (v) {
  return <span style={{color:'#CCC',position:'relative',top:2}}><span className='icon calendar'
                                                                      style={{marginRight:5}}></span><span
    style={{fontSize:13}}><b>{moment(v).format('llll')}</b></span></span>;
};

var Cost = function (v) {
  return <span style={{color:'#19A8F1',position:'relative',top:2}}><span className='icon price'
                                                                         style={{marginRight:5}}></span><span
    style={{fontSize:13}}><b>{"$" + Number(v).toFixed(2)}</b></span></span>;
};

var OnlineSupport = function (v) {
  return <span style={{color:'#FFCC00',position:'relative',top:2}}><span className='icon support'
                                                                         style={{marginRight:5}}></span><span
    style={{fontSize:13}}><b>{Boolean(v).toString()}</b></span></span>;
};

var Header = React.createClass({
  getInitialState(){
    return this.props;
  },
  componentWillReceiveProps(nextProps){
    this.setState(nextProps);
  },
  _getRelatedDOM(title, key, opath){
    if (!this.props[key]) return null;
    return (

      <tr className='related-link'>
        <td colSpan={2} scope="row" style={{width:'100%'}}>
          <Select optionRenderer={function(option){
            if (!option.item[opath + '_deck']){
               return option.label;
            }

            return (
              <div style={{width:'100%',padding:5}}>
                  <Item {...option.item} path={opath}/>
              </div>
            );
          }} name="form-field-name" placeholder={'Select ' + title} options={_.map(this.props[key], function (item, i) {
            return {value: '/' + opath + '/' + item[opath + '_id'], label: item[opath + '_name'], item:item};
          })} onChange={function(path){
            history.pushState(null, path);
          }}/>
        </td>
      </tr>
    )
  },
  getAttributes(){
    var data = this.props;
    return Array.prototype.slice.call(arguments).map(function (k) {
      var key = k[0];
      var name = k.length >= 2 ? k[1] : key;
      var func = k.length >= 3 ? k[2] : function (v) {
        return v
      };
      if (typeof data[key] === 'undefined' || data[key] === null) return;
      return (
        <tr key={key}>
          <th scope="row" style={{textTransform:'capitalize',whiteSpace:'nowrap'}}>{name}</th>
          <td>{func(data[key])}</td>
        </tr>
      );
    })
  },
  render(){
    var tbody;

    var br = (
      <tbody>
      <tr>
        <td colSpan={2} style={{width:'100%',height:10}}/>
      </tr>
      <tr>
        <td colSpan={2} style={{width:'100%',height:2,background:'rgba(255,255,255,0.1)'}}/>
      </tr>
      <tr>
        <td colSpan={2} style={{width:'100%',height:10}}/>
      </tr>
      </tbody>
    );

    switch (this.props.mode) {
      case "game":
        table = (
          <table className="compressed" style={{width:'100%'}}>
            <tbody>{this.getAttributes(["deck"], ["rating"], ["release_date", "Release Date", DateForm],
              ["concepts", "Conepts", Tags], ["genres", "Genres", Tags], ["franchises", "franchises", Tags])}</tbody>
            {br}
            <tbody>
            {this._getRelatedDOM('Publishers', 'publishers', 'company')}
            {this._getRelatedDOM('Developers', 'developers', 'company')}
            {this._getRelatedDOM('Platforms', 'platforms', 'platform')}
            </tbody>
          </table>
        );
        break;
      case "company":
        table = (
          <table className="compressed" style={{width:'100%'}}>
            <tbody>{this.getAttributes(['deck'], ["founded_date", "Founded", DateForm], ["address"], ["city"],
              ["country"], ["state"], ["concepts", "Concepts", Tags], ["phone"], ["website"])}</tbody>
            {br}
            <tbody>
            {this._getRelatedDOM('Developed Games', 'developed_games', 'game')}
            {this._getRelatedDOM('Published Games', 'published_games', 'game')}
            {this._getRelatedDOM('Platforms', 'platforms', 'platform')}
            </tbody>
          </table>
        );
        break;
      case "platform":
        table = (
          <table className="compressed" style={{width:'100%'}}>
            <tbody>{this.getAttributes(['deck'], ["release_date", "Release Date", DateForm], ["online_support", "Online Support", OnlineSupport],
              ["price", "Price", Cost], ["company"], ["install_base", "Install Base"])}</tbody>
            {br}
            <tbody>
            {this._getRelatedDOM('Games', 'games', 'game')}
            {this._getRelatedDOM('Companies', 'companies', 'company')}
            </tbody>
          </table>
        );
        break;
    }

    var backgroundImage = 'url("' + (Array.isArray(this.props.images) ? this.props.images[0] : null) + '")';

    return (
      <div style={{background:'rgba(0,0,0,0.4)',position:'relative'}}>
        <div className='blur'
             style={{width:'100%',height:'100%',top:0,left:0, backgroundImage:backgroundImage,backgroundPosition:'center center',
             backgroundRepeat:'no-repeat',backgroundSize:'cover',backgroundColor:'#555', position:'absolute',zIndex:-1}}/>
        <div className="container" style={{position:'relative'}}>
          <nav className="navbar">
            <ul className="nav navbar-nav">
              <li>
                <Link to="/">Home</Link>
              </li>
              <li>
                <Link to="/about">About</Link>
              </li>
              <li>
                <Link className={this.props.mode === 'game' ? 'active nav-active' : null}
                      to="/games">Games</Link>
              </li>
              <li>
                <Link className={this.props.mode === 'platform' ? 'active nav-active' : null}
                      to="/platforms">Platforms</Link>
              </li>
              <li>
                <Link className={this.props.mode === 'company' ? 'active nav-active' : null}
                      to="/companies">Companies</Link>
              </li>
            </ul>
          </nav>
        </div>
        <div className='page-head' style={{background:'transparent'}}>
          <div className="container">
            <div className='col-md-3'>
              <div
                style={{width:'100%', display:'inline-block', height: 250, borderRadius: 5,backgroundImage: backgroundImage,
                backgroundPosition:'center center',backgroundRepeat:'no-repeat',backgroundSize:'cover',backgroundColor:'#555',
                verticalAlign:'top',marginBottom:10}}
                className='img-rounded'/>
            </div>
            <div className="col-md-9">
              <h1
                style={{display:'inline-block',fontSize:'41px',color:'#FFF',fontWeight:'bold',letterSpacing:'1px',
                textTransform:'uppercase',verticalAlign:'top',marginTop:0}}>{this.props.name}</h1>
              { table }
            </div>
          </div>
        </div>
      </div>
    )
  }
});

module.exports = Header;