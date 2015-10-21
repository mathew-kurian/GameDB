var goog = require('../google/images');
var page0 = require('./platforms/page0.json');
var async = require('async');
var fs = require('fs');

async.eachSeries(page0, function (platform, callback) {
  goog({
    q: platform.name,
    tbs: 'isz:l'
  }, function (err, links) {
    if (err) console.error(err);
    if (platform.image.medium_url)
      links.push(platform.image.medium_url);
    platform.images = links;
    setTimeout(callback, 1000);
  });
}, function () {
  fs.writeFileSync('./platforms/page0.json', JSON.stringify(page0, null, 4), {encoding: 'utf8'});
  console.log('Done!');
});