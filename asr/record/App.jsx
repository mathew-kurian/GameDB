var React = require('react');
var Header = require('./Header.jsx');

function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}

var App = React.createClass({
  getInitialState() {
    window.props.images = shuffle(window.props.images || []);
    return window.props;
  },
  componentDidMount() {
    document.title = this.state.name;
  },
  _handleImgError: function (ref_id) {
    var node = React.findDOMNode(this.refs[ref_id]);
    node.style.display = 'none';
  },
  render() {

    var self = this;
    var videos = this.state.videos || [];

    if (videos.length % 2 === 1) {
      videos.push(null);
    }

    var videoRows = [];

    for (var i = 0; i < videos.length; i += 2) {
      videoRows.push(
        <div className="row" key={i}>
          <div className="col-md-6">
            <iframe style={{marginBottom:20}} className='full-width'
                    src={videos[i].embed_url}
                    width="500" height="213" frameBorder="0" allowFullScreen></iframe>
          </div>
          {videos[i + 1] ? <div className="col-md-6">
            <iframe style={{marginBottom:20}} className='full-width'
                    src={videos[i + 1].embed_url}
                    width="500" height="213" frameBorder="0" allowFullScreen></iframe>
          </div> : null }
        </div>
      );
    }

    return (
      <div style={{width:'100%'}}>
        <Header {...this.state} />

        <div className='container' style={{marginTop:40}}>
          <div className='col-md-9' role='main'>
            <h1>Summary</h1>

            <div className="lead"
                 dangerouslySetInnerHTML={{__html:(this.state.summary || this.state.description || "No summary found").replace(/<a[^>]*>(.*?)<\/a>/g,"$1")}}></div>

            <br />

            { videoRows.length ? <div>
              <h3>Related Videos</h3>

              <p>Watch walkthroughs, gameplays, and trailers</p>
              {videoRows}
            </div> : null}
            <div style={{height:30}}></div>
          </div>
          <div className='col-md-3' role='complementary'>
            <h4>Related Images</h4>

            <p>Get the latest screenshots, logos, and covers</p>
            {this.state.images.slice().splice(1, 3).map(function (url, i) {
              return (<img src={url} key={i} ref={'img' + i} onError={self._handleImgError.bind(null, 'img' + i)}
                           className="img-rounded full-width"/>)
            })}
            <div style={{height:30}}></div>
          </div>
        </div>
      </div>
    )
  }

});

module.exports = App;