var request = require('request');
var async = require('async');
var fs = require('fs');
var _ = require('underscore');

var games = require('./games.json');
var platforms = require('./platforms.json');
var companies = require('./companies.json');

for (var g in games) {
  var game = games[g];
  if (!game.platforms) {
    console.log(game.name);
    game.platforms = [];
  }

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

platforms = _.toArray(platforms);
companies = _.toArray(companies);
games = _.toArray(games);

fs.writeFileSync('./connected/companies.json', JSON.stringify(companies, null, 2), {encoding: 'utf8'});
fs.writeFileSync('./connected/platforms.json', JSON.stringify(platforms, null, 2), {encoding: 'utf8'});
fs.writeFileSync('./connected/games.json', JSON.stringify(games, null, 2), {encoding: 'utf8'});