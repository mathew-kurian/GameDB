var request = require('request');
var async = require('async');
var fs = require('fs');
var tokens = require('./tokens.json');
var _ = require('underscore');

var games = [];

request('https://www.igdb.com/api/v1/games/search?token=' + tokens.token1 + '&filters[hypes_gt]=20', function (error, response, body) {
  if (!error && response.statusCode == 200) {
    games = JSON.parse(body).games;
    async.eachSeries(games, function (game, callback) {
      request('https://www.igdb.com/api/v1/games/' + game.id + '?token=' + tokens.token1, function (error, response, body) {
        _.extend(game, JSON.parse(body).game);
        callback();
      });
    }, function () {
      fs.writeFile('./games/hyped0.json', JSON.stringify(games, null, 4), {encoding: 'utf8'});
      console.log('done');
    })
  } else {
    console.error(error);
    callback();
  }
});