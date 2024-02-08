'use strict';
var fs = require('fs');
var q = require('q');
var readline = require('readline');
var twitterClient = require('./twitterClient');


function get_tweet_ids(path) {
  var deferred = q.defer();
  var rl = readline.createInterface({
    input: fs.createReadStream(path)
  });

  var ner_data_dict = {}
  rl.on('line', (line) => {
    var id, start, end, type;
    [id, start, end, type] = line.split('\t')
    if (!ner_data_dict[id]) {
      ner_data_dict[id] = {};
      ner_data_dict[id]['start_end_list'] = []
    }
    ner_data_dict[id]['start_end_list'].push([start, end, type])
  });

  rl.on('close', () => {
    deferred.resolve(ner_data_dict);
  })
  return deferred.promise;
}


if (require.main == module) {
  get_tweet_ids('../../resources/twitter_tr_dataset_ner_annotations.txt')
    .then(function(result) {
      var ner_data_dict = result;
      var tweet_ids = Object.keys(ner_data_dict).slice(1);
      fs.writeFileSync('ner_tweets.json', '');
      for (var i = 0; i < Math.ceil(tweet_ids.length/100); i++) {
        var start = i*100;
        var end = i*100+100;
        
        twitterClient.lookupTweets(tweet_ids.slice(start, end))
          .then(function(tweets) {
            tweets.forEach((item) => {
              var id = item.id_str;
              ner_data_dict[id]['text'] = item.text;
              ner_data_dict[id]['named_entities'] = [];
              var cur_index = 0;
              item.text.split(/[ ,]+/).forEach((word) => {
                while(word[0] != item.text[cur_index]) {
                  cur_index += 1;
                }
                var hunted = false;
                for (var i in ner_data_dict[id]['start_end_list']) {
                  var s, e, type;
                  [s, e, type] = ner_data_dict[id]['start_end_list'][i];
                  if (parseInt(s) <= cur_index && cur_index <= parseInt(e)) {
                    ner_data_dict[id]['named_entities'].push([word, type]);
                    hunted = true;
                    break;
                  }
                }
                if (!hunted) {
                  ner_data_dict[id]['named_entities'].push([word, 'O']);
                }

                cur_index += word.length;
              });
              fs.appendFile('ner_tweets.json', JSON.stringify(ner_data_dict[id]['named_entities']) + '\n');
            });
          })
      }
    });
}

