var request = require('request');
var async = require('async');
var fs = require('fs');
var _ = require('underscore');

var MAX = 2;

var games = {};
var platforms = {};
var companies = {};

function multiRequest(path, cb) {
  var done;
  async.forEachOfSeries(JSON.parse(fs.readFileSync('./tokens.json')), function (token, key, callback) {
    if (done) return callback();
    var fullPath = path + '?api_key=' + token + '&format=json';
    request(fullPath, function (err, res, body) {
      var entity;
      try {
        entity = JSON.parse(body).results;
      } catch (e) {
        console.error(body);
        return callback();
      }

      if (!entity.id) {
        return callback();
      }

      console.info('Downloaded', entity.name, fullPath);
      cb(entity);
      done = true;
      callback();
    });
  }, function () {
    if (!done) {
      forceWrite();
      console.error("Waiting for 15 mins...");
      setTimeout(function () {
        multiRequest(path, cb);
      }, 16 * 60 * 1000).ref();
    }
  });
}

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

var dlPlatformsOnlyOnce = false;
function downloadPlatforms(callback) {
  if (dlPlatformsOnlyOnce) return;
  dlPlatformsOnlyOnce = true;

  var dlPlatforms = {};
  async.forEachOfSeries(platforms, function (platform, key, callback) {
    multiRequest(platform.api_detail_url, function (dlPlatform) {
      dlPlatforms[dlPlatform.id] = dlPlatform;
      callback();
    });
  }, function () {
    platforms = dlPlatforms;
    callback();
  })
}

function downloadCompany(comp, callback) {
  if (companies[comp.id]) return callback();
  companies[comp.id] = true;

  multiRequest('http://www.giantbomb.com/api/company/' + comp.id, function (dlcomp) {

    var published_games = dlcomp.published_games.slice(0).splice(0, MAX);
    var developed_games = dlcomp.developed_games.slice(0).splice(0, MAX);

    dlcomp.published_games = published_games;
    dlcomp.developed_games = developed_games;
    dlcomp.concepts = _.compact(_.pluck(dlcomp.concepts, 'name').splice(0, 5));

    delete dlcomp.characters;
    delete dlcomp.locations;
    delete dlcomp.objects;
    delete dlcomp.people;

    companies[dlcomp.id] = JSON.parse(JSON.stringify(dlcomp));

    getRelatedGamesAndPlatforms(published_games);
    getRelatedGamesAndPlatforms(developed_games);

    setTimeout(callback, 500);

    function getRelatedGamesAndPlatforms(gs) {
      async.eachSeries(gs, function (game, callback) {

        if (games[game.id]) return callback();
        games[game.id] = true;

        multiRequest(game.api_detail_url, function (dlgame) {

          if (dlgame.platforms) {
            for (var i = 0; i < dlgame.platforms.length; i++) {
              platforms[dlgame.platforms[i].id] = dlgame.platforms[i];
            }
          }

          if (dlgame.publishers) {
            for (var i = 0; i < Math.min(MAX, dlgame.publishers.length); i++) {
              companyQueue.push(dlgame.publishers[i]);
            }

            dlgame.publishers = dlgame.publishers.splice(0, MAX);
          }

          if (dlgame.developers) {
            for (var i = 0; i < Math.min(MAX, dlgame.developers.length); i++) {
              companyQueue.push(dlgame.developers[i]);
            }

            dlgame.developers = dlgame.developers.splice(0, MAX);
          }

          games[dlgame.id] = JSON.parse(JSON.stringify(dlgame));

          process.nextTick(callback);

        });
      }, function () {
        console.error('Finished', dlcomp.name);
      });
    }
  });
}

companyQueue.push({id: 1, name: "Electronic Arts"});
companyQueue.push({id: 1088, name: "Blizzard Entertainment"});

process.on('exit', forceWrite);
process.on('SIGINT', forceWrite);
process.on('uncaughtException', forceWrite);

companyQueue.drain = finish;
