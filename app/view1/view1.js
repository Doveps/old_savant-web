'use strict';

angular.module('myApp.view1', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view1', {
    templateUrl: 'view1/view1.html',
    controller: 'View1Ctrl'
  });
}])

.controller('View1Ctrl', [ '$scope', function($scope) {
  $scope.name = '';
  $scope.names = [{name:"Chris"}, {name:"Calvin"}];
  $scope.addName = function() {
    $scope.names.push( {'name':$scope.name} );
    $scope.name = '';
  };
}]);

/*
.controller('View1Ctrl', [ '$http', function MyCtrl1 ($scope, $http) {
  $http.get("http://localhost:5000/snapshots").then(function(response) {
    $scope.snapshots = response.data;
  });
}]);

.controller('View1Ctrl', [function() {

}]);

.controller('View1Ctrl', [function($scope, $http) {
  $http.get("http://localhost:5000/snapshots").then(function(response) {
    $scope.snapshots = response.data;
  });
}]);
*/
