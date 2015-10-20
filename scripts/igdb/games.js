var request = require('request');
var async = require('async');
var fs = require('fs');
var tokens = require('./tokens.json');

var pages = [];
for (var i = 0; i <= 50; i+=25) pages.push(i);

async.each(pages, function (page, callback) {
  var db = [];

  request('https://www.igdb.com/api/v1/games?token=' + tokens.token1 + '&limit=25&offset=' + page, function (error, response, body) {
    if (!error && response.statusCode == 200) {
      console.log(body);
    } else {
      console.error('Error page' + page);
      callback();
    }
  });
}, function () {
  console.log('Done');
});