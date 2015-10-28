var json2csv = require('json2csv');
var _ = require('underscore');
var fs = require('fs');

var data = [];

var fields = ['game', 'company', 'relation'];

require('./connected/games.json').forEach(function (game) {
  (game.publishers || []).forEach(function (company) {
    data.push({game: game.id, company: company.id, relation: 'publisher'});
  });
  (game.developers || []).forEach(function (company) {
    data.push({game: game.id, company: company.id, relation: 'developer'});
  });
});

json2csv({data: data, fields: fields},
  function (err, csv) {
    if (err) console.log(err);
    fs.writeFileSync('./csv/games-companies.csv', csv, {encoding: 'utf8'});
  });