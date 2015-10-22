var goog = require('../google/images');
var async = require('async');
var fs = require('fs');

async.eachSeries(fs.readdirSync('./db'), function (file, callback) {
  var data = require('./db/' + file);
  async.eachSeries(data, function (data, callback) {
    goog({
      q: data.name,
      tbs: 'isz:l'
    }, function (err, links) {
      if (err) console.error(err);
      if (data.image && data.image.medium_url) {
        links.unshift(data.image.medium_url);
      }
      data.images = links;
      setTimeout(callback, 1000);
    });
  }, function () {
    fs.writeFileSync('./db/' + file, JSON.stringify(data, null, 4), {encoding: 'utf8'});
    console.log(file);
    callback();
  });
}, function () {
  console.log('Done!');
});