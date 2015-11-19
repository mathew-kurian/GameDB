var React = require('react');
var Header = require('./Header.jsx');
var _ = require('underscore');
var request = require('superagent');
var Select = require('react-select');
var abilities = require('./abilities.json');

var Item = React.createClass({
  getInitialState(){
    return {}
  },
  render(){
    return (
      <div className='flex full'>
        <div className='box full'>
          {this.props.name}
          <div
            style={{letterSpacing:0,fontSize:12,textTransform:'none',opacity:0.5}}>{this.props.description}</div>
        </div>
      </div>
    )
  }
});

var App = React.createClass({
  getInitialState() {
    return this._getStateFromProps(this.props);
  },
  _getStateFromProps(props){
    var state = {};

    if (!props) {
      state.name = 'Not found';
      state.deck = 'Provided model and id cannot be found in database';
    } else {
      state.id = props.params.id;
      state.model = props.params.model;
      state.mode = props.params.model;
    }

    return state;
  },
  _fetchLOL(){
    var self = this;
    if (this.state.id == '24024' && !this.state.abilities) {
      this.lolAbilitiesReq = request.get('http://hardcarry.me/api/abilities/')
        .end(function (err, res) {
          self.lolAbilitiesReq = null;

          if (err || res.status !== 200) {
            self.setState({abilities});
            return;
          }

          try {
            self.setState({abilities: res.body});
          } catch (e) {
            // ignore
          }
        });
    }
  },
  _fetch(){
    var self = this;

    this.req = request.get('/api/' + this.state.model + '/' + this.state.id)
      .end(function (err, res) {
        self.req = null;

        if (err || res.status !== 200) {
          self.setState(self._getStateFromProps());
          return;
        }

        try {
          var data = res.body.results[0];
          data.videos = _.pluck(data.videos, 'source').splice(0, 4);
          data.images = shuffle(_.pluck(data.images, 'source'));
          self.setState(data);
        } catch (e) {
          self.setState(self._getStateFromProps());
        }
      });
  },
  _setIFrameSrc(){
    var iframes = document.getElementsByTagName('iframe');
    for (var i = 0; i < iframes.length; i++) {
      var src = iframes[i].getAttribute('data-src');
      iframes[i].contentWindow.location.replace(src);
    }
  },
  componentWillUnmount: function () {
    if (this.req) {
      this.req.abort();
    }

    if (this.lolAbilitiesReq) {
      this.lolAbilitiesReq.abort();
    }
  },
  componentDidMount() {
    this._fetch();
    this._fetchLOL();
  },
  componentDidUpdate(){
    this._setIFrameSrc();
  },
  componentWillReceiveProps(nextProps){
    if (this.req) {
      this.req.abort();
    }

    if (this.lolAbilitiesReq) {
      this.lolAbilitiesReq.abort();
    }

    this.setState(this._getStateFromProps(nextProps));
    setTimeout(this._fetch, 500);
    setTimeout(this._fetchLOL, 500);
  },
  _handleImgError (ref_id) {
    var node = React.findDOMNode(this.refs[ref_id]);
    node.style.display = 'none';
  },
  render() {

    document.title = this.state.name;

    var self = this;
    var videos = this.state.videos || [];

    if (videos.length % 2 === 1) {
      videos.push(null);
    }

    var videoRows = [];
    var description = this.state.description;

    if ((description && description.length < 50) || !description) {
      description = 'No summary found'
    }

    description = description.replace(/<a[^>]*>(.*?)<\/a>/g, "$1");

    for (var i = 0; i < videos.length; i += 2) {
      videoRows.push(
        <div className="row" key={i}>
          <div className="col-md-6">
            <iframe style={{marginBottom:20}} className='full-width' data-src={videos[i]} width="500" height="213"
                    frameBorder="0" allowFullScreen></iframe>
          </div>
          {videos[i + 1] ? <div className="col-md-6">
            <iframe style={{marginBottom:20}} className='full-width' data-src={videos[i + 1]} width="500" height="213"
                    frameBorder="0" allowFullScreen></iframe>
          </div> : null }
        </div>
      );
    }

    var widget;
    if (this.state.id == '24024') {

      var ability = this.state.activeAbility;
      if (ability){
        ability = this.state.abilities[ability];
      }

      var self = this;

      widget = (
        <div style={{border:'1px solid #555',borderRadius:10,padding:20}}>
          <div style={{fontSize:10,fontWeight:400,textTransform:'uppercase',letterSpacing:1,marginBottom:10}}>Ability
            Lookup -
            Powered by HardCarry.me
          </div>
          <Select optionRenderer={function(option){
            return (
              <div style={{width:'100%',padding:5}}>
                  <Item {...option.item}/>
              </div>
            );
          }} name="form-field-test" value={this.state.activeAbility} placeholder={'Select Ability'} options={_.map(this.state.abilities, function (item) {
            return {value: item.name, label: item.name, item:item};
          })} onChange={function(name){
            self.setState({activeAbility: name});
          }}/>
          { ability ? <div>
            <h3>{ability.name}</h3>
            <div style={{marginBottom:5,marginTop:-5}}>
              <div className="columns">costype: {ability.costType}</div>
              <div className="columns">maxrank: {ability.maxrank}</div>
            </div>
            <p>{ability.description}</p>
          </div> : null}
        </div>
      );
    }

    return (
      <div style={{width:'100%'}}>
        <Header {...this.state} />

        <div className='container' style={{marginTop:40}}>
          <div className='col-md-9' role='main'>
            {widget}
            <h1>Summary</h1>

            <div className="lead"
                 dangerouslySetInnerHTML={{__html:description}}></div>

            <br />

            { videoRows.length ? <div>
              <h3>Related Videos</h3>

              <p>Watch walkthroughs, gameplays, and trailers</p>
              {videoRows}
            </div> : null}
            <div style={{height:30}}></div>
          </div>
          <div className='col-md-3' role='complementary'>
            { Array.isArray(this.state.images) ?
            <div>
              <h4>Related Images</h4>

              <p>Get the latest screenshots, logos, and covers</p>
              {this.state.images.slice().splice(1, 3).map(function (url, i) {
                return (<img src={url.replace(/^https/, 'http')} key={i} ref={'img' + i}
                             onError={self._handleImgError.bind(null, 'img' + i)}
                             style={{display:'block'}} className="img-rounded full-width"/>)
                })}
              <div style={{height:30}}></div>
            </div>
              : null }
          </div>
        </div>
      </div>
    )
  }

});

module.exports = App;