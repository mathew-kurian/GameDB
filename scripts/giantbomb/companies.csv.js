var json2csv = require('json2csv');
var _ = require('underscore');
var fs = require('fs');
var moment = require('moment');

var NULL = 'NULL';

var fields = [
  {
    label: 'id',
    value: 'id',
    default: NULL
  }, {
    label: 'name',
    value: 'name',
    default: NULL
  }, {
    label: 'founded_date',
    value: function (row) {
      if (row.date_founded)
        return new Date(row.date_founded)
    },
    default: NULL
  }, {
    label: 'address',
    value: 'location_address',
    default: NULL
  }, {
    label: 'city',
    value: 'location_city',
    default: NULL
  }, {
    label: 'country',
    value: 'location_country',
    default: NULL
  }, {
    label: 'state',
    value: 'location_state',
    default: NULL
  }, {
    label: 'deck',
    value: 'deck',
    default: NULL
  }, {
    label: 'concepts',
    value: function (row) {
      if (Array.isArray(row.concepts) && row.concepts.length) {
        return row.concepts.join(';');
      }
    },
    default: NULL
  }, {
    label: 'phone',
    value: 'phone',
    default: NULL
  }, {
    label: 'website',
    value: 'website',
    default: NULL
  }, {
    label: 'description',
    value: 'description',
    default: NULL
  }];

json2csv({data: require('./connected/companies.json'), fields: fields},
  function (err, csv) {
    if (err) console.log(err);
    fs.writeFileSync('./csv/companies.csv', csv, {encoding: 'utf8'});
  });