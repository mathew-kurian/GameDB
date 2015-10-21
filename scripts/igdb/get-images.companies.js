var goog = require('../google/images');
var page0 = require('./companies/best0.json');
var async = require('async');
var fs = require('fs');

async.eachSeries(page0, function (company, callback) {
  goog({
    q: company.name + ' game company',
    tbs: 'isz:l'
  }, function (err, links) {
    if (err) console.error(err);
    company.images = links;
    delete company.links;
    setTimeout(callback, 1000);
  });
}, function () {
  fs.writeFileSync('./companies/best0.json', JSON.stringify(page0, null, 4), {encoding: 'utf8'});
  console.log('Done!');
});