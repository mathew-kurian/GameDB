['games','companies','platforms'].forEach(function(e){
    var entity = require('./json/' + e + '.json');
    var fs = require('fs');
    var cheerio = require('cheerio');

    entity.forEach(function(entity){
        var $ = cheerio.load(entity.description || '');
        entity.description = $('p').text() || entity.description;
    });

    fs.writeFileSync('./json/' + e + '.nohtml.json', JSON.stringify(entity, null, 2));
});