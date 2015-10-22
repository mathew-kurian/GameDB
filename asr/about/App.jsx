var React = require('react');
var Header = require('./Header.jsx');

var App = React.createClass({
  getInitialState() {
    return window.props;
  },
  componentDidMount() {
    document.title = this.state.title;
  },
  render() {
    return (
      <div style={{width:'100%'}}>
        <Header {...this.state} />

        <div className='container' style={{marginTop:40}}>
          <div className='col-md-9' role='main'>
            <h1>Overview</h1>

            <p className="lead">{this.state.overview}</p>

            <p>Insert all your text here</p>

            <br />

            <div style={{height:30}}></div>
          </div>
          <div className='col-md-3' role='complementary'>
            <h4>Important Attributes</h4>

            <div style={{height:30}}></div>
          </div>
        </div>
      </div>
    )
  }

});

module.exports = App;