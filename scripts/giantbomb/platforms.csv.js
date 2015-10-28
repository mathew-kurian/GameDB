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
    label: 'release_date',
    value: function (row) {
      if (row.release_date)
        return new Date(row.release_date)
    },
    default: NULL
  }, {
    label: 'online_support',
    value: 'online_support',
    default: NULL
  }, {
    label: 'price',
    value: function (row) {
      if (!isNaN(row.original_price))
        return Number(row.original_price);
    },
    default: NULL
  }, {
    label: 'company',
    value: 'company.name',
    default: NULL
  }, {
    label: 'deck',
    value: 'deck',
    default: NULL
  }, {
    label: 'install_base',
    value: 'install_base',
    default: NULL
  }, {
    label: 'description',
    value: 'description',
    default: NULL
  }];

json2csv({data: require('./connected/platforms.json'), fields: fields},
  function (err, csv) {
    if (err) console.log(err);
    fs.writeFileSync('./csv/platforms.csv', csv, {encoding: 'utf8'});
  });