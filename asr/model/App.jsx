var React = require('react');
var Header = require('./Header.jsx');
var FixedDataTable = require('fixed-data-table');

var Table = FixedDataTable.Table;
var Column = FixedDataTable.Column;

var SortTypes = {
  ASC: 'ASC',
  DESC: 'DESC'
};

var App = React.createClass({
  getInitialState() {
    var props = window.props;
    props.width = 825 - 60;
    return props;
  },
  _updateTableWidth: function () {
    var node = React.findDOMNode(this.refs.tableBox);
    var currWidth = node.offsetWidth - 60;
    if (currWidth !== this.state.width) {
      this.setState({width: node.offsetWidth - 60});
    }
  },
  componentDidMount() {
    var self = this;

    this._updateTableWidth();

    window.onresize = function () {
      self._updateTableWidth();
    }
  },
  _headerRenderer: function (label, cellDataKey) {
    return <div style={{color:'#fff',cursor:'pointer'}} onClick={this._sortRowsBy.bind(null, cellDataKey)}>{label}</div>
  },
  _sortRowsBy(cellDataKey) {
    var sortDir = this.state.sortDir;
    var sortBy = cellDataKey;
    if (sortBy === this.state.sortBy) {
      sortDir = this.state.sortDir === SortTypes.ASC ? SortTypes.DESC : SortTypes.ASC;
    } else {
      sortDir = SortTypes.DESC;
    }

    var rows = this.state.rows.slice();
    rows.sort((a, b) => {
      var sortVal = 0;
      if (a[sortBy] > b[sortBy]) {
        sortVal = 1;
      }
      if (a[sortBy] < b[sortBy]) {
        sortVal = -1;
      }

      if (sortDir === SortTypes.DESC) {
        sortVal = sortVal * -1;
      }

      return sortVal;
    });

    this.setState({
      rows,
      sortBy,
      sortDir
    });
  },
  render() {

    var self = this;
    var sortDirArrow = '';

    if (this.state.sortDir !== null) {
      sortDirArrow = this.state.sortDir === SortTypes.DESC ? ' ↓' : ' ↑';
    }

    function rowGetter(rowIndex) {
      return self.state.rows[rowIndex];
    }

    var videos = this.state.videos;

    if (videos.length % 2 === 1) {
      videos.push(null);
    }

    var videoRows = [];

    for (var i = 0; i < videos.length; i += 2) {
      videoRows.push(
        <div className="row" key={i}>
          <div className="col-md-6">
            <iframe style={{marginBottom:10}} className='full-width'
                    src={videos[i]}
                    width="500" height="213" frameBorder="0" allowFullscreen></iframe>
          </div>
          {videos[i + 1] ? <div className="col-md-6">
            <iframe style={{marginBottom:10}} className='full-width'
                    src={videos[i + 1]}
                    width="500" height="213" frameBorder="0" allowFullscreen></iframe>
          </div> : null }
        </div>
      );
    }

    return (
      <div style={{width:'100%'}}>
        <Header {...this.state} />

        <div className='container' style={{marginTop:40}}>
          <div className='col-md-9' role='main'>
            <h1>Overview</h1>

            <p className="lead">{this.state.overview}</p>

            <div className='table-box' ref='tableBox'>
              <div className='title'>Model</div>
              <Table rowHeight={37} rowGetter={rowGetter} rowsCount={this.state.rows.length} width={this.state.width}
                     height={38 * (this.state.rows.length + 1)}
                     headerHeight={37}>{
                this.state.columns.map(function (col, i) {
                  return (
                    <Column label={col + (self.state.sortBy === i ? sortDirArrow : '')} key={i}
                            width={Math.max(100, self.state.width/self.state.columns.length)} dataKey={i}
                            headerRenderer={self._headerRenderer}/>
                  )
                })}
              </Table>
            </div>
            <br />

            <h3>Related Videos</h3>

            <p>Get the lowdown on the key pieces of Bootstrap's infrastructure, including our approach</p>

            {videoRows}
            <div style={{height:40}}></div>
          </div>
          <div className='col-md-3' role='complementary'>
            <h4>Related Images</h4>
            {this.state.images.map(function (url, i) {
              return (<img src={url} key={i}
                           className="img-rounded full-width"/>)
            })}
          </div>
        </div>
      </div>
    )
  }

});

module.exports = App;