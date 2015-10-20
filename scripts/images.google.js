var client = require('google-images');
var fs = require('fs');
var request = require('request');
var async = require('async');
var cheerio = require('cheerio');
var files = fs.readdirSync('./games');

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

var key = 'Covers';

async.eachSeries(files, function(file, callback){
    var games = require('./games/' + file);
    var dl = 0;
    console.log('Started ' + file);
    async.eachSeries(games, function(game, callback){
        // if (game[key] && game[key].length > 12) return callback();
        var q = game.Title + ' ps4 front cover';
        request({
            url: 'https://www.google.com/search?q=' + encodeQuery(q) + '&tbm=isch&&tbs=isz:l',
            method: 'get',
            headers: {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
                'accept-encoding':'gzip, deflate, sdch',
                'accept-language':'en-US,en;q=0.8,de;q=0.6',
                'cache-control':'max-age=0',
                'dnt':1,
                'referer':'https://www.google.com/search?q=' + encodeQuery(q) + '&tbs=isz:l&tbm=isch'  // MUST change every 50 or so requests
            },
            gzip: true
        },function(err, res, body){
            if (err) return callback();
            var links = [];

            try {
                links = body.match(/<a href=\"(.*?)\" jsaction=\"fire.ivg_o;mouseover:str.hmov;mouseout:str.hmou\" class=\"rg_l\">/g)
                            .map(function(a){    
                    return decodeURIComponent(decodeURIComponent(a.match(/imgres\?imgurl=(.*?)\&amp;imgrefurl=/)[0].replace('imgres\?imgurl=', '').replace('&amp;imgrefurl=', '')));
                });
            } catch(e){
                console.error(game.Title, encodeQuery(q));
            }

            dl++;

            game[key] = links;
            setTimeout(callback, 400); // dont trigger the google scrape detector
        });
    }, function(){
        console.log('Finished ' + file);
        fs.writeFileSync('./games/' + file, JSON.stringify(games, null, 2), {encoding: 'utf8'});
        if (dl > 5){
            console.log('Waiting for 5 seconds...');
            setTimeout(callback, 5000);
        } else {
            setTimeout(callback, 1000);  // dont trigger the google scrape detector
        }
    });
}, function(){
    console.log('Done!');
});