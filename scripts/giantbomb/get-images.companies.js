var goog = require('../google/images');
var page0 = require('./companies/page0.json');
var async = require('async');
var fs = require('fs');

async.eachSeries(page0, function (company, callback) {
  goog({
    q: company.name,
    tbs: 'isz:l'
  }, function (err, links) {
    if (err) console.error(err);
    if (company.image && company.image.medium_url)
      links.unshift(company.image.medium_url);
    company.images = links;
    setTimeout(callback, 1000);
  });
}, function () {
  fs.writeFileSync('./companies/page0.json', JSON.stringify(page0, null, 4), {encoding: 'utf8'});
  console.log('Done!');
});