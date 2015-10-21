var request = require('request');
var async = require('async');
var fs = require('fs');
var tokens = require('./tokens.json');
var _ = require('underscore');

var best = [];
var files = fs.readdirSync('./companies');

for (var c = 0; c < files.length; c++) {
  var file = require('./companies/' + files[c]);
  for (var i = 0; i < file.length; i++) {
    var company = file[i];
    if (company.founded_year && company.average_rating && company.company_logo && company.parent) {
      company.average_rating = Number(Number(company.average_rating).toFixed(2));
      best.push(company);
    }
  }
}

fs.writeFileSync('./companies/best0.json', JSON.stringify(best, null, 4), {encoding: 'utf8'});