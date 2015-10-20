var goog = require('../google/images');
var hyped0 = require('./games/hyped0.json');
var async = require('async');
var fs = require('fs');

async.eachSeries(hyped0, function (game, callback) {
  goog({
    q: game.name + ' front cover',
    tbs: 'isz:l'
  }, function (err, links) {
    if (err) console.error(err);
    game.images = links;
    delete game.links;
    setTimeout(callback, 1000);
  });
}, function () {
  fs.writeFileSync('./games/hyped0.json', JSON.stringify(hyped0, null, 4), {encoding: 'utf8'});
  console.log('Done!');
});