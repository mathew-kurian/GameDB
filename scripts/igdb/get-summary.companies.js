var request = require('request');
var async = require('async');
var fs = require('fs');
var tokens = require('./tokens.json');
var _ = require('underscore');

request('https://www.igdb.com/api/v1/companies?token=' + tokens.token1, function (error, response, body) {
  if (!error && response.statusCode == 200) {
    var companies = JSON.parse(body).companies;
    fs.writeFile('./companies/page0.json', JSON.stringify(companies, null, 4), {encoding: 'utf8'});
    console.log('done');
  }
});