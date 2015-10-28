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
        return new Date(row.original_release_date);
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

json2csv({data: require('./connected/games.json'), fields: fields},
  function (err, csv) {
    if (err) console.log(err);
    fs.writeFileSync('./csv/games.csv', csv, {encoding: 'utf8'});
  });