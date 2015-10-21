var fs = require('fs');
var request = require('request');
var tokens = require('tokens.json');

request({
  url: 'http://www.giantbomb.com/api/platforms/?sort=release_date:desc&api_key=' + tokens.token1 + '&format=json',
  headers: {
    'Accept': 'application/json'
  }
}, function (error, res, body) {
  if (!error && res.statusCode == 200) {
    fs.writeFileSync('./platforms/page0.json', JSON.stringify(JSON.parse(body).results, null, 2), {encoding: 'utf8'});
  }
});