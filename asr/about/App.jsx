var React = require('react');
var Header = require('./Header.jsx');
var brace = require('brace');
var AceEditor = require('react-ace');
var request = require('superagent');

require('brace/mode/python');
require('brace/theme/monokai');

var App = React.createClass({
  getInitialState() {
    return this.props.route;
  },
  componentDidMount() {
    document.title = this.state.title;
  },
  runTests(){
    if (this.state.running) {
      return false;
    }

    var self = this;
    this.setState({running: true});

    request
      .get('/run-tests?__id=' + Date.now())
      .end(function (err, res) {
        if (err) {
          console.error(err);
        } else {
          self.setState({console: (self.state.console || '') + '\n' + res.text})
        }

        self.setState({running: false});
      });

  },
  render() {
    return (
      <div style={{width:'100%'}}>
        <Header {...this.state} />

        <div className='container about' style={{marginTop:40}}>
          <div className='col-md-6' role='main'>
            <h1>4Play Vitals</h1>

            <ul>
              <li>Total commits: 230</li>
              <li>Total issues: 42</li>
              <li>Unit tests: 23</li>
              <li><a href="http://docs.games10.apiary.io/#">Apiary Documentation</a></li>
              <li><a href="https://github.com/bluejamesbond/cs373-idb/">Public Repository</a></li>
              <li><a href="https://github.com/bluejamesbond/cs373-idb/wiki">Wiki</a></li>
              <li><a href="https://github.com/bluejamesbond/cs373-idb/issues">Issue Tracker</a></li>
            </ul>

            <h2>Sources</h2>
            <ul>
              <li><a href="http://www.giantbomb.com/api/">GiantBomb</a> provided a REST API for their game data. Using
                NodeJS scripts and graph traversal techniques, we were able to download games, platforms, and companies.
              </li>
              <li><a href="http://images.google.com/">Google Images</a> allowed (not exactly) us to scrape for
                images. Techniques such as DOM manipulation via. JQuery, we were able to extract images. We also spoofed
                the header in order to get the "large" images for best quality on the webpages.
              </li>
              <li><a href="https://www.igdb.com/api/v1/documentation/">IGDB</a> with their well-documented a set of REST
                api
                endpoints which helped us collect more detailed information about the games. We found different media
                such as logos, walkthroughs, and screenshots. We hope to acquire more information in Phase 2 such as
                rating and game priace.
              </li>
            </ul>

            <h3>Test Console</h3>

            <a onClick={this.runTests}
               style={{opacity:this.state.running ? 0.5 : 1, color: '#000', padding: '4px 6px', fontSize: 12, fontWeight: 400, background: '#CCC',borderRadius: 3, textTransform: 'uppercase', display: 'inline-block', letterSpacing: 1, marginTop: 0, marginBottom: 10,cursor:'pointer',textDecoration: 'none'}}>run
              unit tests</a>

            <div style={{width:'100%',height:400,borderRadius:4,overflow:'hidden'}}>
              <AceEditor mode="python" readOnly={true} theme="monokai"
                         value={this.state.console || 'No tests have been run'}
                         name="unit-tests" editorProps={{$blockScrolling: true}} height="100%" width='100%'/>
            </div>

            <div style={{height:30}}></div>
          </div>
          <div className='col-md-6' role='complementary'>
            <div className="flex row m">
              <div className="box" style={{paddingRight:20}}>
                <div className="profile-rounded"
                     style={{backgroundImage:'url(/assets/dist/images/cathy-0.jpg)'}}/>
              </div>

              <div className="box">
                <h5>Cathy Feng</h5>

                <p>I moved here from China in 2005 and was vastly disappointed that drive thrus were, in fact, not
                  robots
                  who brought your food out for you. Other than that I've been pretty satisfied with the US and hope
                  to get a job in something that has nothing to do with threads and concurrency one day. During phase 1
                  most of my effort was put into the technical report, writing ~1/3 of it as well as editing. I made 3
                  commits, did not make any issues and have not yet written any unit tests in phase 1. In phase 2,
                  I added 3 commits and 2 unit tests. In phase 3, I added 2 commits, created the presentation and critiques, and
                  contributed heavily to the technical report.</p>
              </div>
            </div>
            <hr />


            <div className="flex row m">
              <div className="box" style={{paddingRight:20}}>
                <div className="profile-rounded"
                     style={{backgroundImage:'url(/assets/dist/images/matt-0.jpg)'}}/>
              </div>

              <div className="box">
                <h5>Matthew Kim</h5>

                <p>Student at the University of Texas at Austin completing a bachelor's degree in Computer Science. This
                  is my final semester, and I plan on building a career in software engineering after graduation.
                  During this project, I worked on creating the unit tests and the data models. During my time working
                  in phase 1, I submitted 4 commits and wrote 9 unit tests. In phase 2, I added 9 commits and 8 unit tests. I was
                  project lead in phase 3 and added 8 commits, as well as 5 unit tests for the search. In addition, I lead the creation
                  process for the user stories.</p>
              </div>
            </div>
            <hr />


            <div className="flex row m">
              <div className="box" style={{paddingRight:20}}>
                <div className="profile-rounded"
                     style={{backgroundImage:'url(/assets/dist/images/rahul-0.jpg)'}}/>
              </div>

              <div className="box">
                <h5>Rahul Rajavel</h5>

                <p>Computer Science and Electrical Engineering Double Major Student at the
                  University of Texas at Austin. This is my 3rd year. My hobbies are basketball and tennis.
                  During the project, I focused on documentation, working on the Apiary and the UML diagram, and on unit tests.
                  I made 11 commits, filed 5 issues, wrote 0 unit tests in phase 1. In phase 2, I made 31 commits,
                  filed 4 issues, and wrote 10 unit tests. I was also the project lead during phase 2. I added 35 commits
                  during phase 3, contributing slightly to the search feature.</p>
              </div>
            </div>
            <hr />


            <div className="flex row m">
              <div className="box" style={{paddingRight:20}}>
                <div className="profile-rounded" style={{backgroundImage:'url(/assets/dist/images/mat-0.jpg)'}}/>
              </div>

              <div className="box">
                <h5>Mathew Kurian</h5>

                <p>Student at the University of Texas at Austin completing a dual major in Computer Science and
                  Electrical
                  Engineering. This is my final year and I will be joining Salesforce fulltime. In my free time, I like
                  to mix it up with a little bit of lifting, reading, and biking waiting for the finishline. During the
                  project, I focused on developing the front end and working with React. I had fun being the Project
                  Lead during Phase 1 during which I submitted 59 commits, filed 14 issues, wrote 3 unit tests. I added
                  75 commits in phase 2. I added 61 commits in phase 3, leading the group in creation of the search feature.</p>
              </div>
            </div>

            <div style={{height:30}}></div>
          </div>
        </div>
      </div >
    )
  }

});

module.exports = App;
