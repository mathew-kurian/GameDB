var pm2 = require('pm2');
var express = require('express');
var program = require('commander');

program
  .version('0.0.1')
  .option('-p, --port <n>', 'Port', parseInt, 5000)
  .option('-a, --action <n>', 'Action', String, '')
  .option('-pp, --python_port <n>', 'Python Port', parseInt, 6000)
  .parse(process.argv);

if (program.action == 'main') {

  var listenPort = parseInt(process.env.pm_id) + program.port;
  var redirectPort = parseInt(process.env.pm_id) + program.python_port;

  console.log(listenPort, redirectPort);

  pm2.connect(() => {
    pm2.start({
      exec_command: __dirname + '/index.py',
      script: __dirname + '/index.py',
      args: ` -p ${redirectPort}`,
      instances: 1,
      name: `python-server-${process.env.pm_id}`,
      interpreter: 'python3',
      max_memory_restart: '150M'
    }, function (err, apps) {
      console.log(err);
      console.log(apps);
    });
  });

  var app = express();

  app.get('/*', (req, res) => {
    res.redirect(`http://localhost:${redirectPort}/req.path`);
  });

  app.listen(listenPort, () => {
    console.log('Load balancer on', listenPort);
  });
} else {
  pm2.connect(()=> {
    pm2.start({
      script: __filename,
      args: ` -p ${program.port} -a main -pp ${program.python_port}`,
      exec_mode: 'cluster',
      instances: 1,
      node_args: ["--harmony"],
      max_memory_restart: '150M'
    }, () => {
      console.log(arguments);
      pm2.disconnect();
    });
  });
}