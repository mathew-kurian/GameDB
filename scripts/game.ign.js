var cheerio = require('cheerio');
var async = require('async');
var request = require('request');
var fs = require('fs');

function getLinks($) {
    var links = [];
    $(".game-title a").each(function() {
        links.push($(this).attr('href'))
    });
    return links;
}

function getDetails($, a, to) {
    $(a).each(function() {
        var text = $(this).text().replace(/\n/g, ' ');
        to[text.substring(0, text.indexOf(":")).trim()] = text.substring(text.indexOf(":") + 1).trim()
    });
    return to;
}

function getReleases($) {
    var releases = [];
    $("#editions ul").each(function() {
        var data = getDetails($, ".editions-details div", {});
        data.Region = $(this).find('.editions-region').text();
        data.Cover = $(this).find('.editions-boxart img').attr('src');
        releases.push(data);
    });
    return releases;
}

var db = [];
var pages = [];

for (var i = 0; i <= 1000; i+= 50) pages.push(i);

async.each(pages, function(page, callback){
    request('http://www.ign.com/games/ps4', function(error, response, html) {
        if (!error && response.statusCode == 200) {
            var $ = cheerio.load(html);
            var links = getLinks($);
            async.eachSeries(links, function(link, callback) {
                request('http://www.ign.com' + link, function(error, response, html) {
                    $ = cheerio.load(html);
                    console.log(html);
                    var data = getDetails($, ".gameInfo-list div", {});
                    data.Summary = $("#summary p").text().trim();
                    data.Rating = Number($(".ratingValue").eq(0).text().trim());
                    data.Releases = getReleases($);
                    db.push(data);
                    callback();
                });
            }, function() {
                fs.writeFile('./games/db1.json', JSON.stringify(db), {
                    encoding: 'utf8'
                });

                callback();
            });
        }
    });
}, function(){
    console.log('Done');
});