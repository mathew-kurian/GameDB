var json2csv = require('json2csv');
var _ = require('underscore');
var fs = require('fs');
var moment = require('moment');
var path = require('object-path');

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
      if (row.release_date) {
        return moment(row.release_date).toDate();
      }
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

var data = [];

require('./connected/platforms.json').forEach(function (game) {
  var obj = {};
  fields.forEach(function (field) {
    obj[field.label] = (typeof field.value === 'string' ? path.get(game, field.value) : field.value(game)) || null;
  });
  data.push(obj);
});

json2csv({data: require('./connected/platforms.json'), fields: fields},
  function (err, csv) {
    if (err) console.log(err);
    fs.writeFileSync('./json/platforms.json', JSON.stringify(data, null, 2));
    fs.writeFileSync('./csv/platforms.csv', csv, {encoding: 'utf8'});
  });