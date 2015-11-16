var file = './json/games.json';
var table = require(file);

table.forEach(function(t){
  t.entity = 'game';
});

require('fs').writeFileSync(file, JSON.stringify(table, null, 2), "utf8");