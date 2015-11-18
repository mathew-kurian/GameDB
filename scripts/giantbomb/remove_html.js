['games','companies','platforms'].forEach(function(e){
    var entity = require('./json/' + e + '.json');
    var fs = require('fs');
    var cheerio = require('cheerio');

    entity.forEach(function(entity){
        var $ = cheerio.load('<body>' + (entity.description || '') + '</body>');
        $('h1').remove();
        $('h2').remove();
        $('h3').remove();
        $('h4').remove();
        $('h5').remove();
        $('h6').remove();
        $('table').remove();

        entity.description = ($('body').text() || entity.description || '').replace(/ +(?= )/g,'');

    });

    fs.writeFileSync('./json/' + e + '.nohtml.json', JSON.stringify(entity, null, 2));
});