var json2csv = require('json2csv');
var async = require('async');
var fs = require('fs');

var data = [];

async.eachSeries(fs.readdirSync('./connected'), function (file, callback) {
  require('./connected/' + file).forEach(function (a) {
    var count = 0;
    (a.videos || []).forEach(function (video) {
      if (typeof video !== 'string') return;
      if (video.length !== 41) return;
      if (count++ > 10) return;
      data.push({relation: file.replace('.json', ''), id: a.id, video: video});
    });
  });

  callback();
}, function () {
  json2csv({data: data, fields: ['id', 'video', 'relation']},
    function (err, csv) {
      if (err) console.log(err);
      fs.writeFileSync('./csv/videos.csv', csv, {encoding: 'utf8'});
      fs.writeFileSync('./csv/videos.json', JSON.stringify(data, null, 2));
    });
});