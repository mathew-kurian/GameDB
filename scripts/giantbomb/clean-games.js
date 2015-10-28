var games = require('./connected/games.json');
var fs = require('fs');

games.forEach(function(game){
    game.videos = [];
    game._images = game.images;
    game.images = [];
});

fs.writeFileSync('./connected/games.json', JSON.stringify(games, null, 2));