var React = require('react');
var request = require('superagent');
var ReactBlur = require('react-blur');

var Search = React.createClass({
  getInitialState(){
    return {results: []};
  },
  _handleInput(e){
    var input = e.target.value;

    this.refs.close.classList.add('rotate');

    if (this.req) {
      this.req.abort();
      this.req = null;
    }

    if (!input.trim().length) {
      this.refs.close.classList.remove('rotate');
      return this.setState({results: [], input: ''});
    }

    var self = this;
    this.req = request.get('http://4playdb.me/api/search?q=name:' + encodeURIComponent(input) + '^4*%20deck:' + encodeURIComponent(input) + '*^2')
      .end(function (err, res) {
        self.refs.close.classList.remove('rotate');
        if (err || res.status !== 200) return self.req = null;
        try {
          self.setState({results: res.body.results, input: input});
        } catch (e) {
          // ignore
        }
      });
  },
  _handleResize(){
    if (this.refs.game) {
      this.refs.game.style.height = this.refs.platform.style.height =
        this.refs.company.style.height = window.innerWidth < 992 ? 'auto' : '100%';
      this.refs.game.style.overflow = this.refs.platform.style.overflow =
        this.refs.company.style.overflow = window.innerWidth < 992 ? 'hidden' : 'scroll';
    }
  },
  componentDidUpdate: function () {
    this.refs.input.focus();
    this._handleResize();
  },
  getResultsFor(a){

    var i = 0;
    var children = [];

    this.state.results.forEach(function (res) {
      if (res.entity !== a) return;
      children.push(
        <div key={i++} className="row"
             style={{padding: 20,borderBottom: '1px solid rgba(255,255,255,0.0)',position:'relative',overflow:'hidden',margin:0}}>
          <ReactBlur
            style={{opacity:0.3,width:'100%',height:'100%',top:0,left:0,backgroundPosition:'center center',backgroundColor:'#000', position:'absolute',zIndex:-1}}
            img={res.images[0].source} blurRadius={50}/>
          <div className="col-xs-4">
            <div className='col' style={{ borderRadius: 3, display: 'inline-block', marginRight: 10, position: 'relative',
                    top: -2, verticalAlign: 'middle',backgroundImage:"url('" + res.images[0].source + "')",
                    backgroundSize:'cover', height:50, width: '100%',marginRight:10,
                    backgroundPosition:'center center',marginBottom:10}}/>
          </div>
          <div className='col-xs-8'>
            <div style={{color:'rgba(255,255,255,0.7)'}} dangerouslySetInnerHTML={{__html:res.name}}/>
            <div
              style={{letterSpacing:0,fontSize:12,textTransform:'none',color:'rgba(255,255,255,0.4)'}}
              dangerouslySetInnerHTML={{__html:res.deck}}></div>
            <div
              style={{letterSpacing:0,fontSize:10,textTransform:'none',color:'rgba(255,255,255,0.2)'}}
              dangerouslySetInnerHTML={{__html:res.description}}></div>
          </div>
        </div>
      )
    });

    return <div ref={a}
                style={{borderRight:'1px solid rgba(255,255,255,0.0)', padding:0,position:'relative',height:'100%',minHeight:100}}
                className="col-md-4 scroll scroll-y">
      <div style={{textTransform:'uppercase',letterSpacing:'1px',fontWeight:700,color:'#555',padding:10}}>{a}</div>
      { children.length ? children : <div className="empty">Not found</div>}
    </div>
  },
  onClose(){
    if (this.req) {
      this.req.abort();
      this.req = null;
    }

    window.removeEventListener('resize', this._handleResize);

    document.documentElement.style.overflow = 'auto';

    this.setState({search: false, input: false, results: []});
  },
  onOpen(){
    this._handleResize = this._handleResize.bind(this);
    window.addEventListener('resize', this._handleResize);
    this._handleResize()
    this.refs.root.classList.remove('opacity-0');
    document.documentElement.style.overflow = 'hidden';
    this.refs.input.focus();

    this.setState({search: true});
    this.refs.input.value = '';
  },
  render(){

    return (
      <div>
        <input ref='input' onClick={this.onOpen}
               placeholder="Search"
               style={{float:'right',margin:18,color:'#FFF',fontSize:'12px',letterSpacing:'1px',textTransform:'uppercase',
                 position:'relative',zIndex:4,marginRight:0,width:200,padding:7,
                 background:'rgba(255,255,255,0.16)',border:'none', outline:'none',borderRadius:5}}/>
        <div ref='root' className="full transition-slow"
             style={{position:'fixed',transform:'translate3d(0,' + (this.state.search ? 0 : (screen.height + 'px')) + ',0)',background:this.state.input ? '#111' : 'transparent',
             zIndex:4,left:0,top:0,right:0,bottom:0}}>
          <div
            style={{background:'#333',width:'100%',position:'relative',boxShadow:'0 0px 50px rgba(16, 16, 16, 0.49)'}}>
            <input ref="input"
                   onChange={this._handleInput}
                   placeholder="Begin typing..."
                   style={{lineHeight:'40px',background:'transparent',border:'none',margin:0,fontSize:20,padding:20,paddingRight:50,color:'#fff',
          width:'100%'}}/>
            <div style={{position:'absolute',right:0,top:0,bottom:0,width:50}}>
              <div className='full icon close search-close transition' ref="close"
                   onClick={this.onClose}>
              </div>
            </div>
          </div>
          <div style={{position:'absolute',top:80,left:0,right:0,bottom:0}}
               onClick={this.state.input ? null : this.onClose}>
            { this.state.input ? <div className="row" style={{margin:0,overflow:'auto',height:'100%'}}>
              {this.getResultsFor('game')}
              {this.getResultsFor('company')}
              {this.getResultsFor('platform')}
            </div> : null }
          </div>
        </div>
      </div>
    )
  }
});


module.exports = Search;