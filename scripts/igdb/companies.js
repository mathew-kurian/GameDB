var request = require('request');
var async = require('async');
var fs = require('fs');
var tokens = require('./tokens.json');
var _ = require('underscore');

var pages = [];
for (var i = 2650; i < 6925; i += 25) pages.push(i);

async.eachSeries(pages, function (page, callback) {
  request('https://www.igdb.com/api/v1/companies?token=' + tokens.token1 + '&offset=' + page, function (error, response, body) {
    if (!error && response.statusCode == 200) {
      var companies = JSON.parse(body).companies;
      async.eachSeries(companies, function (company, callback) {
        request('https://www.igdb.com/api/v1/companies/' + company.id + '?token=' + tokens.token1, function (error, response, body) {
          _.extend(company, JSON.parse(body).company);
          console.log(company.name);
          callback();
        });
      }, function () {
        fs.writeFileSync('./companies/page' + page + '.json', JSON.stringify(companies, null, 4), {encoding: 'utf8'});
        console.info("Finished " + page);
        callback();
      });
    }
  });
}, function () {
  console.log('Done!');
});