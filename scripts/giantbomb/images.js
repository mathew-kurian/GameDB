var goog = require('../google/images');
var async = require('async');
var fs = require('fs');

async.eachSeries(fs.readdirSync('./connected'), function (file, callback) {
  var data = require('./connected/' + file);
  if (file.indexOf('platforms') !== 0) return callback();
  async.eachSeries(data, function (data, callback) {
    //if (data.images.length > 10) {
    //  console.info('Skipping', data.name);
    //  return callback();
    //}
    goog({
      q: data.name,
      tbs: 'isz:l'
    }, function (err, links) {
      if (err) console.error(err);
      if (data.image && data.image.medium_url) {
        links.unshift(data.image.medium_url);
      }
      delete data.image;
      data.images = links;
      console.log(data.name);
      setTimeout(callback, 200);
    });
  }, function () {
    fs.writeFileSync('./connected/' + file, JSON.stringify(data, null, 4), {encoding: 'utf8'});
    console.log(file);
    callback();
  });
}, function () {
  console.log('Done!');
});