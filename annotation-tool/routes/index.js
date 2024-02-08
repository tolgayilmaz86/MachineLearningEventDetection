var express = require('express');
var router = express.Router();
var path = require('path');
const readline = require('readline');
const fs = require('fs');

var annotated_ids = new Set();
var ids_to_be_annotated;
var pool = {};

var lines = fs.readFileSync(path.join(__dirname, '../resources/hurriyet_caddesi.json'), 'utf-8').split('\n');

lines.forEach((line) => {
  JSON.parse(line).forEach((tweet) => {
    pool[tweet.tweetId] = tweet.text;
  });
});

lines = fs.readFileSync(path.join(__dirname, '../resources/annotated.json'), 'utf-8').split('\n');

lines.forEach((line) => {
  try {
    annotated_ids.add(JSON.parse(line)['id']);
  } catch(exception) {
  }
});

ids_to_be_annotated = Object.keys(pool).filter(id => !annotated_ids.has(id));
ids_to_be_annotated = new Set(ids_to_be_annotated);

/* GET home page. */
router.use(express.static(path.join(__dirname, '../node_modules')));
router.use(express.static(path.join(__dirname, '../public')));

router.get('/', function(req, res) {
  res.sendFile(path.join(__dirname, '../public/index.html'));
});

router.get('/tweet/', function(req, res) {
  var tweetId = [...ids_to_be_annotated][0];
  console.log(ids_to_be_annotated.size);
  res.json({id: tweetId, text: pool[tweetId], remaining: ids_to_be_annotated.size});
});

router.post('/tweet', function(req, res) {
  ids_to_be_annotated.delete(req.body.id);
  fs.appendFileSync(path.join(__dirname,'../resources/annotated.json'), JSON.stringify(req.body) + "\n");
  res.send('success');
})


module.exports = router;
