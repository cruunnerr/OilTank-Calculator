var mysql = require('mysql');
var fs = require('fs');
var PromiseFtp = require('promise-ftp');
var connection = mysql.createConnection({
  host: 'ip.to.the.server',
  port: '3307', // mostly port 3306 is used, but my synology is using port 3307
  user: 'username',
  password: 'password',
  database: 'Tank'
});

connection.connect();

connection.query('SELECT * from Volumen', function(err, results, fields) {
    if(err) throw err;

    fs.writeFile('table.json', JSON.stringify(results), function (err) {
      if (err) throw err;
      console.log('Saved!');
    });
});

connection.end();


var host = "ip.to.the.server"
var user = "username"
var password = "password"
var ftp = new PromiseFtp();
  ftp.connect({
  host: host, 
  user: user, 
  password: password
  })
  .then(function (serverMessage) {
    return ftp.put('table.json', 'web/table.json');
  }).then(function () {
    return ftp.end();
  });
