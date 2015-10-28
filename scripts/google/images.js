var fs = require('fs');
var request = require('request');
var async = require('async');
var cheerio = require('cheerio');

encodeQuery = function (q) {
  return q.replace(/\$/g, "%24")
    .replace(/\+/g, '%2B')
    .replace(/\s/g, '+')
    .replace(/&/g, "%26")
    .replace(/\//g, "%2F")
    .replace(/\=/g, "%3D")
    .replace(/%/g, "%25")
    .replace(/@/g, "%40")
    .replace(/#/g, "%23")
    .replace(/\?/g, "%3F")
    .replace(/;/g, "%3B")
    .replace(/,/g, "%2C")
    .replace(/['’]/g, "%27");
};

module.exports = function (opts, callback) {
  var q = encodeQuery(opts.q);
  var params = '';

  delete opts.q;

  opts.tbs = opts.tbs || 'isz:l';
  opts.tbm = opts.tbm || 'isch';

  for (var a in opts) {
    params += a + '=' + encodeURIComponent(opts[a]) + '&';
  }

  request({
    url: 'https://www.google.com/search?' + params + '&q=' + q,
    method: 'get',
    headers: {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
      'accept-encoding': 'gzip, deflate, sdch',
      'accept-language': 'en-US,en;q=0.8,de;q=0.6',
      'cache-control': 'max-age=0',
      'dnt': 1,
      'referer': 'https://www.google.com/search?q=' + encodeQuery(q) + '&tbs=isz:l&tbm=isch'  // MUST change every 50 or so requests
    },
    gzip: true
  }, function (err, res, body) {
    if (err) return callback(err, []);

    var links = [];

    try {
      links = body.match(/imgres\?imgurl=(.*?)\&amp;imgrefurl=/gm)
        .map(function (imgurl) {
          imgurl = imgurl.replace('imgres\?imgurl=', '').replace('&amp;imgrefurl=', '');
          return decodeURIComponent(decodeURIComponent(imgurl));
        });
    } catch (e) {
      console.log(body);
      console.error(q, params);
      return callback(e, []);
    }
    
    callback(0, links);
  });
};