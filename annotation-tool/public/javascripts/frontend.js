'use strict';

angular.module('annotationTool', ['ngMaterial']).
config(function($mdThemingProvider) {
  // $mdThemingProvider.theme('default')
  //   .primaryPalette('blue')
  //   .accentPalette('red');
});

angular.module('annotationTool')
  .controller('annotationController', function($http) {
    var vm = this;
    var annotated = [];
    
    vm.labels = [
      {icon: 'date_range', 'name': 'date'},
      {icon: 'person', name: 'person'},
      {icon: 'message', name: 'DM'},
      {icon: 'warning', name: 'event'},
      {icon: 'swap_horiz', name: 'preposition'},
      {icon: 'group', name: 'organization'},
      {icon: 'location_on', name: 'location'},
      {icon: 'blur_on', name: 'other'}
    ];
    vm.highlightIndex = 0;

    vm.getNext = function () {
      $http.get('/tweet').then(function(response) {
        vm.tweetId = response.data.id;
        vm.tweet = response.data.text.split(/[ ,!?]+/);
        vm.remaining = response.data.remaining;
        
        console.log(vm.tweet);
        vm.tweet.forEach(function(word) {

        })

        annotated = vm.tweet.map(function(item) {
          return [item, 'OTHER']
        });

        vm.highlightIndex = 0;
      });
    }

    vm.getNext();

    vm.annotateAndGetNext = function() {
      $http.post('/tweet', JSON.stringify({id: vm.tweetId, annotated: annotated}));
      vm.getNext();
    }

    vm.annotate = function(index, tag) {
      var word = vm.tweet[index];
      annotated[index] = [word, tag.toUpperCase()];
      vm.highlightIndex += 1;
      console.log(annotated);
      console.log(vm.highlightIndex);
      if (vm.tweet.length <= vm.highlightIndex) {
        $http.post('/tweet', JSON.stringify({id: vm.tweetId, annotated: annotated}));
        vm.getNext();
      }
    };
  });

angular.module('annotationTool')
  .factory('Tweets', function($http) {
    var service = {}
  
    service.getRawTweets = function() {
      return $http.get('/tweet').then(function(response) {
        vm.tweet = response.data;
      })
    };

    return service;
  })