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
    label: 'rating',
    value: function (row) {
      if (Array.isArray(row.original_game_rating) &&
        row.original_game_rating.length) {
        return row.original_game_rating[0].name
      }
    },
    default: NULL
  }, {
    label: 'release_date',
    value: function (row) {
      if (row.original_release_date)
        return moment(row.original_release_date).toDate();
      if (row.expected_release_year)
        return moment(row.expected_release_year +
          ' ' + row.expected_release_month, 'YYYY MM').toDate();
    },
    default: NULL
  }, {
    label: 'deck',
    value: 'deck',
    default: NULL
  }, {
    label: 'concepts',
    value: function (row) {
      if (Array.isArray(row.concepts) && row.concepts.length) {
        return _.pluck(row.concepts, 'name').join(';');
      }
    },
    default: NULL
  }, {
    label: 'genres',
    value: function (row) {
      if (Array.isArray(row.genres) && row.genres.length) {
        return _.pluck(row.genres, 'name').join(';');
      }
    },
    default: NULL
  }, {
    label: 'franchises',
    value: function (row) {
      if (Array.isArray(row.franchises) && row.franchises.length) {
        return _.pluck(row.franchises, 'name').join(';');
      }
    },
    default: NULL
  }, {
    label: 'description',
    value: 'description',
    default: NULL
  }];

var data = [];

require('./connected/games.json').forEach(function (game) {
  var obj = {};
  fields.forEach(function (field) {
    obj[field.label] = (typeof field.value === 'string' ? path.get(game, field.value) : field.value(game)) || null;
  });
  data.push(obj);
});

json2csv({data: require('./connected/games.json'), fields: fields},
  function (err, csv) {
    if (err) console.log(err);
    fs.writeFileSync('./json/games.json', JSON.stringify(data, null, 2));
    fs.writeFileSync('./csv/games.csv', csv, {encoding: 'utf8'});
  });