var json2csv = require('json2csv');
var async = require('async');
var fs = require('fs');

var data = [];

async.eachSeries(fs.readdirSync('./connected'), function (file, callback) {
  require('./connected/' + file).forEach(function (a) {
    var count = 0;
    (a.images || []).forEach(function (image) {
      if (typeof image === 'object') image = image.super_url;
      if (typeof image !== 'string') return;
      if (count++ > 10) return;
      data.push({relation: file.replace('.json', ''), id: a.id, image: image});
    });
  });

  callback();
}, function () {
  json2csv({data: data, fields: ['id', 'image', 'relation']},
    function (err, csv) {
      if (err) console.log(err);
      fs.writeFileSync('./csv/images.csv', csv, {encoding: 'utf8'});
    });
});