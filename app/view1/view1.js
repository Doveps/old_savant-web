'use strict';

angular.module('myApp.view1', ['ngRoute'/*'mgcrea.ngStrap'*/]) //Does that work? ['ngRoute'] 'myApp.view1'

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view1', {
    templateUrl: 'view1/view1.html',
    controller: 'View1Ctrl'
  });
}])


.controller('View1Ctrl', [ '$scope', '$log', '$http', function($scope, $log, $http) {
  $scope.name = '';
  $scope.age;
  $scope.names = [{name:"Chris", age: 10}, {name:"Calvin", age: 15},]; //Those things are hashes. Name set to thing. Thing set to property.
  
  $scope.addName = function() {
    $scope.names.push( {'name':$scope.name, 'age':$scope.age} );
    
    $scope.name = '';
    $scope.age = 0;
    $scope.$log = $log;
    $scope.message = "what";
    log.debug("Does this button work?");
/*
    $scope.ids = '';
    $scope.times = '';

    $scope.things = [{ids:response.data}];
    $log.debug(response.data.secondary_id);
    $scope.things.push({'ids':$scope.ids});
    //$log.debug($scope.names);
*/
  };
   $http({
        method: 'GET',
        url: 'http://localhost:5000/snapshots',
        headers: {'Content-Type':'text/plain'}
     }).then(function successCallback(response){
       $log.debug('hello!!!');
       //$log.debug(response.data);
       var arrayLength = response.data.length;
       var arrayTest = ["Test1", "Test2", "Test3"];
       
       $scope.ids;
       $scope.timestamps;
       $scope.things = [];

       for(var i = 0; i < arrayLength; i++){
         //$log.debug(arrayTest[i]);
         //console.log(arrayTest[i]);
         $log.debug(response.data[i].secondary_id);

         $scope.things.push({'ids':response.data[i].secondary_id, 'timestamps':response.data[i].timestamp, 'converted':convertTime(response)});
         //Converting timestmap to time? I'm not actually sure if this is a timecode or just seconds... 
         
         //Er... I dunno... Fiddle with this?

         
       }
      /*
      $scope.addThings = function(){
        $scope.things.push({'thing1':$scope.thing1});

      }
     */
    }, function errorCallback(response){
       $log.debug('hello!?');
       //$log.debug(response.data);
     }
    
     );
    
     /*
     $http.get("http://jsonplaceholder.typicode.com/").then(function(response){
       $log.debug(response.data);
       
     });
     */
     /*
     $http.get("http://jsonplaceholder.typicode.com/").then(function(response){
       //$scope.snapshots = response.data;
       //$log.debug($scope.snapshots);
       $log.debug(response.data); 
     });
     */
    
    function convertTime(response){
      var date = new Date(response.data[i].timestamp)
      return date.getDate();
    }
    
}]);

//http://localhost:5000/snapshots
/*
$scope.id;
$scope.things = [{id: $scope.snapshots.secondary_id}];
$scope.addThing = function(){
  

}
*/

/*
function createCORSRequest(method, url){
  var xhr = new XMLHttpRequest();

}
*/