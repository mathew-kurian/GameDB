var goog = require('../google/youtube');
var async = require('async');
var fs = require('fs');

async.eachSeries(['games.json']/*fs.readdirSync('./connected')*/, function (file, callback) {
  var data = require('./connected/' + file);
  async.eachSeries(data, function (data, callback) {
    if (data.images.length > 5) {
     console.info('Skipping', data.name);
     return callback();
    }
    goog({
      q: data.name
    }, function (err, links) {
      if (err) console.error(err);
      data.videos = links;
      console.log(data.name);
      setTimeout(callback, 200);
    });
  }, function () {
    fs.writeFileSync('./connected/' + file, JSON.stringify(data, null, 4));
    console.log(file);
    callback();
  });
}, function () {
  console.log('Done!');
});