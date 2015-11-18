var React = require('react');
var request = require('superagent');

var Search = React.createClass({
  getInitialState(){
    return {results: []};
  },
  componentWillUnmount: function () {
    if (this.req) {
      this.req.abort();
      this.req = null;
    }

    document.documentElement.style.overflow = 'auto';
  },
  _handleInput(e){
    var input = e.target.value;

    if (this.req) {
      this.req.abort();
      this.req = null;
    }

    if (!input.trim().length) {
      return this.setState({results: []});
    }

    var self = this;
    this.req = request.get('http://104.130.23.111:80/api/search?q=name:' + encodeURIComponent(input) +'^4*%20deck:' + encodeURIComponent(input) +'*^2')
      .end(function (err, res) {
        if (err || res.status !== 200) return self.req = null;
        try {
          self.setState({results: res.body.results});
        } catch (e) {
          // ignore
        }
      });
  },
  componentDidMount: function () {
    this.refs.root.classList.remove('opacity-0');
    document.documentElement.style.overflow = 'hidden';
  },
  getResultsFor(a){

    var children = [];

    this.state.results.forEach(function (res, i) {
      if (res.entity !== a) return;
      children.push(
        <div key={i}>
          <div className='flex' style={{padding: 20,borderBottom: '1px solid rgba(255,255,255,0.1)',position:'relative',overflow:'hidden'}}>
            <div className='blur'
                 style={{opacity:0.3,width:'100%',height:'100%',top:0,left:0, backgroundImage:"url('" + res.images[0].source + "')",backgroundPosition:'center center',
             backgroundRepeat:'no-repeat',backgroundSize:'cover',backgroundColor:'#000', position:'absolute',zIndex:-1}}/>
            <div className='box' style={{ borderRadius: 3, display: 'inline-block', marginRight: 10, position: 'relative',
                    top: -2, verticalAlign: 'middle',backgroundImage:"url('" + res.images[0].source + "')",
                    backgroundSize:'cover', height:50, width: 50, maxWidth: 50, minWidth: 50, marginRight:10,
                    backgroundPosition:'center center'}}/>
            <div className='box'>
              <div style={{color:'rgba(255,255,255,0.5)'}} dangerouslySetInnerHTML={{__html:res.name}}/>
              <div
                style={{letterSpacing:0,fontSize:12,textTransform:'none',color:'rgba(255,255,255,0.4)'}}
                dangerouslySetInnerHTML={{__html:res.deck}}></div>
              <div
                style={{letterSpacing:0,fontSize:10,textTransform:'none',color:'rgba(255,255,255,0.2)'}}
                dangerouslySetInnerHTML={{__html:res.description}}></div>
            </div>
          </div>
        </div>
      )
    });

    return <div style={{borderRight:'1px solid rgba(255,255,255,0.1)', position:'relative'}} className="box full">
      <div className="full-abs">
        { children.length ? <div className="full scroll scroll-y">{children}</div> : <div className="empty">No {a}&nbsp;found</div>}
      </div>
    </div>
  },
  render(){
    var children;

    children = this.state.results.map(function (res, i) {
      return (
        <div key={i}>
          <div className='flex' style={{padding: 20,borderBottom: '1px solid #333'}}>
            <div className='box' style={{ borderRadius: 3, display: 'inline-block', marginRight: 10, position: 'relative',
                    top: -2, verticalAlign: 'middle',backgroundImage:"url('" + res.images[0].source + "')",
                    backgroundSize:'cover', height:40, width: 30, maxWidth: 30, minWidth: 30, marginRight:10,
                    backgroundPosition:'center center'}}/>
            <div className='box full'>
              {res.name}
              <div
                style={{letterSpacing:0,fontSize:12,textTransform:'none',opacity:0.5}}>{res.deck}</div>
            </div>
          </div>
        </div>
      )
    });

    return (
      <div ref='root' className="full flex vertical animate-1 opacity-0"
           style={{background:'#222',position:'fixed',zIndex:4,left:0,top:0,right:0,bottom:0}}>
        <div style={{background:'#333',width:'100%',position:'relative',boxShadow:'0 0px 50px rgba(16, 16, 16, 0.49)'}}><input
          onChange={this._handleInput}
          placeholder="Search entity"
          style={{lineHeight:'40px',background:'transparent',border:'none',margin:0,fontSize:20,padding:20,paddingRight:50,color:'#fff',
          width:'100%'}}/>
          <div style={{position:'absolute',right:0,top:0,bottom:0,width:50}}>
            <div className='full icon close search-close'
                 onClick={this.props.onClose}>
            </div>
          </div>
        </div>
        <div style={{position:'absolute',top:80,left:0,right:0,bottom:0}}>
          <div className="flex full">
            {this.getResultsFor('game')}
            {this.getResultsFor('company')}
            {this.getResultsFor('platform')}
          </div>
        </div>
      </div>
    )
  }
});


module.exports = Search;