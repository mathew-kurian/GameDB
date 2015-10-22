var request = require('request');
var async = require('async');
var fs = require('fs');
var tokens = require('./tokens.json');
var _ = require('underscore');

var games = {};
var platforms = {};
var companies = {};

var companyQueue = async.queue(function (company, callback) {
  downloadCompany(JSON.parse(JSON.stringify(company)), callback);
}, 2);

function forceWrite() {
  console.log(arguments);
  console.log('Writing files');
  fs.writeFileSync('./companies.json', JSON.stringify(companies, null, 2), {encoding: 'utf8'});
  fs.writeFileSync('./platforms.json', JSON.stringify(platforms, null, 2), {encoding: 'utf8'});
  fs.writeFileSync('./games.json', JSON.stringify(games, null, 2), {encoding: 'utf8'});
}

function finish(msg) {
  console.error(msg);
  downloadPlatforms(forceWrite);
}

function downloadPlatforms(callback) {
  var _platforms = {};
  async.forEachOfSeries(platforms, function (platform, key, callback) {

    console.log('Downloading', platform.name);

    request(platform.api_detail_url + '?api_key=' + tokens.token1 + '&format=json',
      function (error, res, body) {
        var platform = JSON.parse(body).results;
        if (!platform.name) return finish("premature");

        _.extend(_platforms, _.indexBy([platform], 'id'));
        callback();
      })
  }, function () {
    platforms = _platforms;
    callback();
  })
}

function downloadCompany(_company, callback) {
  if (companies[_company.id]) return callback();
  companies[_company.id] = true;

  console.log('Downloading', _company.name);

  request('http://www.giantbomb.com/api/company/' + _company.id + '?api_key=' + tokens.token1 + '&format=json',
    function (error, res, body) {

      var company = JSON.parse(body).results;
      if (!company.name) return finish("premature");

      var published_games = company.published_games.slice(0).splice(0, 1);
      var developed_games = company.developed_games.slice(0).splice(0, 1);

      company.published_games = published_games;
      company.developed_games = developed_games;
      company.concepts = _.compact(_.pluck(company.concepts, 'name').splice(0, 5));

      delete company.characters;
      delete company.locations;
      delete company.objects;
      delete company.people;

      companies[company.id] = JSON.parse(JSON.stringify(company));

      function getRelatedGamesAndPlatforms(_games, callback) {
        async.eachSeries(_games, function (_game, callback) {

          if (games[_game.id]) return callback();
          games[_game.id] = true;

          console.log('Downloading', _game.name);

          request(_game.api_detail_url + '?api_key=' + tokens.token1 + '&format=json',
            function (error, res, body) {

              var game = JSON.parse(body).results;
              if (!game.name) return finish("premature");

              if (game.platforms)
                for (var i = 0; i < game.platforms.length; i++)
                  platforms[game.platforms[i].id] = game.platforms[i];

              if (game.publishers) {
                for (var i = 0; i < Math.min(1, game.publishers.length); i++)
                  companyQueue.push(game.publishers[i]);
                game.publishers = game.publishers.splice(0, 1);
              }

              if (game.developers) {
                for (var i = 0; i < Math.min(1, game.developers.length); i++)
                  companyQueue.push(game.developers[i]);
                game.developers = game.developers.splice(0, 1);
              }

              games[game.id] = JSON.parse(JSON.stringify(game));

              process.nextTick(callback);

            });
        }, function () {
          console.log('Done with games of', company.name);
        });
      }

      getRelatedGamesAndPlatforms(published_games);
      getRelatedGamesAndPlatforms(developed_games);

      setTimeout(callback, 500);

    });
}

companyQueue.push({id: 1, name: "Electronic Arts"});
companyQueue.push({id: 1088, name: "Blizzard Entertainment"});

process.on('exit', forceWrite);
process.on('SIGINT', forceWrite);
//process.on('uncaughtException', forceWrite);

companyQueue.drain = finish;
