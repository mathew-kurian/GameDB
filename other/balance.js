var pm2 = require('pm2');
var express = require('express');
var app = express();
var servers = require('./servers.json');
var index = 0;

app.get('/*', (req, res) => {
  res.redirect(`${servers[index++ % servers.length]}/${req.path}`);
});

app.listen(80, () => {
  console.log('Started server');
});