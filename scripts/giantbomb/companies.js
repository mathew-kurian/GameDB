var fs = require('fs');
var request = require('request');
var tokens = require('./tokens.json');
var async = require('async');
var _ = require('underscore');

request({
  url: 'http://www.giantbomb.com/api/companies?api_key=' + tokens.token1 + '&format=json',
  headers: {
    'Accept': 'application/json'
  }
}, function (error, res, body) {
  if (!error && res.statusCode == 200) {
    var companies = JSON.parse(body).results;
    async.eachSeries(companies, function (company, callback) {
      if (!error && res.statusCode == 200) {
        request('http://www.giantbomb.com/api/company/' + company.id + '?api_key=' + tokens.token1 + '&format=json',
          function (error, res, body) {
            var details = JSON.parse(body).results;
            _.extend(company, details);

            if (Array.isArray(company.published_games))
              company.published_games = _.pluck(company.published_games, 'name').splice(0, 5);
            if (Array.isArray(company.developed_games))
              company.developed_games = _.pluck(company.developed_games, 'name').splice(0, 5);
            if (Array.isArray(company.concepts))
              company.concepts = _.pluck(company.concepts, 'name').splice(0, 5);

            delete company.characters;
            delete company.locations;
            delete company.objects;
            delete company.people;
            callback();
          });
      }
    }, function () {
      fs.writeFileSync('./companies/page0.json', JSON.stringify(companies, null, 2), {encoding: 'utf8'});
    });
  }
});