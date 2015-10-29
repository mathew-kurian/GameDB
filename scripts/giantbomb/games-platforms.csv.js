var json2csv = require('json2csv');
var _ = require('underscore');
var fs = require('fs');

var data = [];

var fields = ['game', 'platform'];

require('./connected/games.json').forEach(function (game) {
  (game.platforms || []).forEach(function (platform) {
    data.push({game: game.id, platform: platform.id});
  });
});

json2csv({data: data, fields: fields},
  function (err, csv) {
    if (err) console.log(err);
    fs.writeFileSync('./csv/games-platforms.csv', csv, {encoding: 'utf8'});
    fs.writeFileSync('./csv/games-platforms.json', JSON.stringify(data, null, 2));
  });