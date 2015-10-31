var React = require('react');
var Header = require('./Header.jsx');

var App = React.createClass({
  getInitialState() {
    return this.props.route;
  },
  componentDidMount() {
    document.title = this.state.title;
  },
  render() {
    return (
      <div style={{width:'100%'}}>
        <Header {...this.state} />

        <div className='container about' style={{marginTop:40}}>
          <div className='col-md-6' role='main'>
            <h1>Overview</h1>

            <p>The purpose of this project to is provide an interactive way to track the dependencies between
              video-games, platforms, and game companies.</p>


            <h2>Vitals</h2>
            <ul>
              <li>Total commits: 70</li>
              <li>Total issues: 23</li>
              <li>Unit tests: 10</li>
              <li><a href="http://docs.games10.apiary.io/#">Apiary Documentation</a></li>
              <li><a href="https://github.com/bluejamesbond/cs373-idb/">Public Repository</a></li>
              <li><a href="https://github.com/bluejamesbond/cs373-idb/wiki">Wiki</a></li>
              <li><a href="https://github.com/bluejamesbond/cs373-idb/issues">Issue Tracker</a></li>
              <li>Total commits: 70</li>
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

            <div style={{height:30}}></div>
          </div>
          <div className='col-md-6' role='complementary'>
            <h1>4Play Team</h1>

            <div className="row">
              <div className="col-md-3">
                <div className="profile-rounded"
                     style={{backgroundImage:'url(https://scontent-dfw1-1.xx.fbcdn.net/hphotos-xpa1/v/t1.0-9/1395936_10204632727451045_3363102470207409449_n.jpg?oh=58c949608e5367b0bc411e0bb42e8864&oe=568FDA40)'}}/>
              </div>

              <div className="col-md-8">
                <h5>Cathy Feng</h5>

                <p>I moved here from China in 2005 and was vastly disappointed that drive thrus were, in fact, not
                  robots
                  who brought your food out for you. Other than that I've been pretty satisfied with the US and hope
                  to get a job in something that has nothing to do with threads and concurrency one day. During phase 1
                  most of my effort was put into the technical report, writing ~1/3 of it as well as editing. I made 3
                  commits, did not make any issues and have not yet written any unit tests.</p>
              </div>
            </div>
            <hr />


            <div className="row">
              <div className="col-md-3">
                <div className="profile-rounded"
                     style={{backgroundImage:'url(https://scontent-dfw1-1.xx.fbcdn.net/hphotos-xpf1/t31.0-8/920083_592830954060541_1859406506_o.jpg)'}}/>
              </div>

              <div className="col-md-8">
                <h5>Mattew Kim</h5>

                <p>Student at the University of Texas at Austin completing a bachelor's degree in Computer Science. This
                  is my final semester, and I plan on building a career in software engineering after graduation.
                  During this project, I worked on creating the unit tests and the data models. During my time working
                  in phase 1, I submitted 4 commits and wrote 9 unit tests.</p>
              </div>
            </div>
            <hr />


            <div className="row">
              <div className="col-md-3">
                <div className="profile-rounded"
                     style={{backgroundImage:'url(https://scontent-dfw1-1.xx.fbcdn.net/hphotos-xft1/t31.0-8/11072903_1623982707825499_467584200074503472_o.jpg)'}}/>
              </div>

              <div className="col-md-8">
                <h5>Rahul Rajavel</h5>

                <p>Computer Science and Electrical Engineering Double Major Student at the
                  University of Texas at Austin. This is my 3rd year. My hobbies are basketball and tennis.
                  During the project, I focused on documentation, working on the Apiary and the UML diagram.
                  I made 11 commits, filed 5 issues, wrote 0 unit tests.</p>
              </div>
            </div>
            <hr />


            <div className="row">
              <div className="col-md-3">
                <div className="profile-rounded" style={{backgroundImage:'url(http://i.imgur.com/5rcNNQU.jpg)'}}/>
              </div>

              <div className="col-md-8">
                <h5>Mathew Kurian</h5>

                <p>Student at the University of Texas at Austin completing a dual major in Computer Science and
                  Electrical
                  Engineering. This is my final year and I will be joining Salesforce fulltime. In my free time, I like
                  to mix it up with a little bit of lifting, reading, and biking waiting for the finishline. During the
                  project, I focused on developing the front end and working with React. I had fun being the Project
                  Lead during Phase 1 during which I submitted 59 commits, filed 14 issues, wrote 3 unit tests.</p>
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
