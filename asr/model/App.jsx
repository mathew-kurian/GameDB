var React = require('react');
var Header = require('../about/Header.jsx');
var FixedDataTable = require('fixed-data-table');
var _ = require('underscore');
var moment = require('moment');
var Path = require('object-path');
var request = require('superagent');

import {Link} from 'react-router'

var Table = FixedDataTable.Table;
var Column = FixedDataTable.Column;

var SortTypes = {
  ASC: 'ASC',
  DESC: 'DESC'
};

var App = React.createClass({
  getInitialState() {
    return this._getStateFromProps(this.props);
  },
  _getStateFromProps: function (props) {
    var model;
    var state;

    if (props) {
      model = props.params.model;
      state = props.route[model];
    }

    if (!state) {
      state = {};
      state.title = 'Not Found';
      state.description = 'Model not found. Available models are games, companies, and platforms';
      state.overview = 'No records found';
      state.theme = '#BBB';
      state.model = 'invalid';
      state.rows = [];
      state.columns = [];
    } else {
      state.model = model;
      state.offset = isNaN(props.location.query.offset) ? 0 : Number(props.location.query.offset);
      state.limit = isNaN(props.location.query.limit) ? 25 : Number(props.location.query.limit);
      state.rows = this.state ? this.state.rows || [] : [];
      state.columns = this.state ? this.state.columns || [] : [];
    }

    state.width = (this.state ? this.state.width : null) || (825 - 60);

    return state;
  },
  _updateTableWidth: function () {
    var node = React.findDOMNode(this.refs.tableBox);
    if (!node) return;
    var currWidth = node.offsetWidth - 60;
    if (currWidth !== this.state.width) {
      this.setState({width: node.offsetWidth - 60});
    }
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

    this.setState(this._getStateFromProps(nextProps));

    setTimeout(()=> {
      this._fetch();
      this._updateTableWidth();
    }, 500);
  },
  componentDidUpdate(){
    this._updateTableWidth();
  },
  _fetch(){

    var self = this;
    this.req = request.get(`/api/${this.state.model}?limit=${this.state.model.limit}&offset=${this.state.offset}`)
      .end(function (err, res) {
        if (err || res.status !== 200) {
          self.setState(self._getStateFromProps());
          return self.req = null;
        }

        try {

          var rows = [], columns = ['id', 'name', 'deck'];

          (res.body.results || []).forEach(function (record) {
            var row = [];
            columns.forEach(function (col) {
              row.push(record[col]);
            });
            rows.push(row);
          });

          self.setState({rows: rows, columns: columns})
        } catch (e) {
          // ignore
        }
      });
  },
  componentDidMount() {
    var self = this;

    this._fetch();
    this._updateTableWidth();

    window.onresize = function () {
      self._updateTableWidth();
    }
  },
  _headerRenderer(label, cellDataKey) {
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
  _cellRenderer(data, column, row){
    if (column > 1)
      return <div
        style={{whiteSpace: 'nowrap', opacity: column > 1 ? 0.5 : 1, textOverflow: 'ellipsis', overflow: 'hidden', width: 250}}>{typeof data === 'string' && data.length > 50 ? data.substring(0, 50) : (this.state.columns[column].indexOf('date') > -1 ? (data ? moment(data).format('lll') : 'TBD') : String(data))}</div>;
    return <Link style={{whiteSpace: 'nowrap'}} to={'/' + this.state.record + "/" + row[0]}>{data}</Link>
  },
  render() {

    var self = this;
    var sortDirArrow = '';

    document.title = this.state.title;

    if (this.state.sortDir !== null) {
      sortDirArrow = this.state.sortDir === SortTypes.DESC ? ' ↓' : ' ↑';
    }

    function rowGetter(rowIndex) {
      return self.state.rows[rowIndex];
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
              { this.state.offset - this.state.limit >= 0 ? <Link className='icon ileft'
                                                                  style={{position: 'absolute',top: 30,right: 65,width:30,height:30,textAlign:'center',lineHeight:'30px'}}
                                                                  to={`/${this.state.model}?offset=${this.state.offset - this.state.limit}&limit=${this.state.limit}`}></Link> : null }
              { this.state.rows.length == this.state.limit ? <Link className='icon iright'
                                                                   style={{position: 'absolute',top: 30,right: 30,width:30,height:30,textAlign:'center',lineHeight:'30px'}}
                                                                   to={`/${this.state.model}?offset=${this.state.limit + this.state.offset}&limit=${this.state.limit}`}></Link> : null }
              <Table rowHeight={37} rowGetter={rowGetter} rowsCount={this.state.rows.length} width={this.state.width}
                     height={Math.min(45 * (this.state.rows.length + 1), 500)}
                     headerHeight={37}>{
                this.state.columns.map(function (col, i) {
                  return (
                    <Column label={col + (self.state.sortBy === i ? sortDirArrow : '')} key={i}
                            width={i ? 250 : 50} dataKey={i}
                            cellRenderer={self._cellRenderer}
                            headerRenderer={self._headerRenderer}/>
                  )
                })}
              </Table>
            </div>
            <br />

            <div style={{height:30}}></div>
          </div>
          <div className='col-md-3' role='complementary'>
            <h4>Important Attributes</h4>
            {(this.state.columns.length ? this.state.columns : ['no attributes']).map(function (col, i) {
              return (<div className="columns" key={i}>{col}</div>)
            })}
            <div style={{height:30}}></div>
          </div>
        </div>
      </div>
    )
  }

});

module.exports = App;