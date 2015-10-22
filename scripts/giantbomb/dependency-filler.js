var request = require('request');
var async = require('async');
var fs = require('fs');
var _ = require('underscore');

var games = require('./games.json');
var platforms = require('./platforms.json');
var companies = require('./companies.json');

for (var g in games) {
  var game = games[g];
  game.platforms.forEach(function (platform) {
    var currPlatform = platforms[platform.id];
    if (!currPlatform.companies) currPlatform.companies = {};
    if (!currPlatform.games) currPlatform.games = {};
    function attach(from) {
      if (game[from]) {
        game[from].forEach(function (company) {
            var currCompany = companies[company.id];
            if (!currCompany.platforms) currCompany.platforms = {};
            currCompany.platforms[currPlatform.id] = platform;
            currPlatform.companies[currCompany.id] = company;
            currPlatform.games[game.id] = {
              "api_detail_url": game.api_detail_url,
              "id": game.id,
              "name": game.name
            }
          }
        );
      }
    }

    attach('developers');
    attach('publishers');

  });
}

for (g in companies) {
  companies[g].platforms = _.toArray(companies[g].platforms, 'id');
}


for (g in platforms) {
  platforms[g].companies = _.toArray(platforms[g].companies, 'id');
  platforms[g].games = _.toArray(platforms[g].games, 'id');
}

fs.writeFileSync('./companies.connected.json', JSON.stringify(companies, null, 2), {encoding: 'utf8'});
fs.writeFileSync('./platforms.connected.json', JSON.stringify(platforms, null, 2), {encoding: 'utf8'});
fs.writeFileSync('./games.connected.json', JSON.stringify(games, null, 2), {encoding: 'utf8'});