webpackJsonp([0],[
/* 0 */
/***/ function(module, exports, __webpack_require__) {

	routeConfig.$inject = ["$urlRouterProvider", "$stateProvider", "$httpProvider", "$resourceProvider"];
	run.$inject = ["$rootScope", "$state", "$stateParams"];
	var angular = __webpack_require__(1);

	__webpack_require__(3);
	__webpack_require__(5);


	angular
	    .module('app', [
	        /*
	         * Angular modules
	         */
	        'ngResource', 'ui.router'

	        /*
	         * 3rd Party modules
	         */
	    ])
	    .config(routeConfig)
	    .constant('BASE_URL', 'http://localhost:8000')
	    .run(run);

	function routeConfig($urlRouterProvider, $stateProvider, $httpProvider, $resourceProvider) {
	    // Enable cors in client side
	    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
	    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

	    // Defaults
	    $urlRouterProvider.otherwise("/");
	    $resourceProvider.defaults.stripTrailingSlashes = false;

	    // Primary routes
	    $stateProvider
	        .state('dashboard', {
	            url: "/",
	            templateUrl: "app/layout.html",
	            abstract: true
	        })
	        .state('dashboard.home', {
	            url: "",
	            templateUrl: "app/home.html",

	        })
	        .state('dashboard.comparisons', {
	            url: "comparisons",
	            templateUrl: "app/comparisons/comparisons.html",
	            controller: "ComparisonListController"
	        })
	        .state('dashboard.comparison', {
	            url: "comparisons/:id",
	            templateUrl: "app/comparisons/comparison-detail.html",
	            controller: "ComparisonDetailController"
	        })
	        .state('dashboard.sets', {
	            url: "sets",
	            templateUrl: "app/sets/sets.html",
	            controller: "SetListController"
	        })
	        .state('dashboard.set', {
	            url: "sets/:id",
	            templateUrl: "app/sets/set-detail.html",
	            controller: "SetDetailController"
	        })
	}

	function run($rootScope, $state, $stateParams) {
	    $rootScope.$state = $state;
	    $rootScope.$stateParams = $stateParams;
	}

	__webpack_require__(6);
	__webpack_require__(7);
	__webpack_require__(10);

/***/ },
/* 1 */,
/* 2 */,
/* 3 */,
/* 4 */,
/* 5 */,
/* 6 */
/***/ function(module, exports) {

	module.exports = function DataService($http, $resource, BASE_URL) {
	    return {
	        comparisons: comparisons,
	        sets: sets
	    };

	    function comparisons() {
	        return $resource('/comparisons/:id/', {id: '@id'}, {
	            'list': {method: 'GET'},
	            'update': {method: 'PUT'},
	            'query': {method: 'GET', isArray: true}
	        });
	    }

	    function sets() {
	        return $resource('/sets/:id/', {id: '@id'}, {
	            'list': {method: 'GET'},
	            'update': {method: 'PUT'},
	            'query': {method: 'GET', isArray: true}
	        });
	    }
	}

/***/ },
/* 7 */
/***/ function(module, exports, __webpack_require__) {

	var angular = __webpack_require__(1);

	angular
	    .module('app')
	    .controller("SetDetailController", __webpack_require__(8))
	    .controller("SetListController", __webpack_require__(9));


/***/ },
/* 8 */
/***/ function(module, exports) {

	module.exports = function ($scope) {

	};



/***/ },
/* 9 */
/***/ function(module, exports) {

	module.exports = function ($scope) {

	};



/***/ },
/* 10 */
/***/ function(module, exports, __webpack_require__) {

	var angular = __webpack_require__(1);

	angular
	    .module('app')
	    .controller("ComparisonDetailController", __webpack_require__(11))
	    .controller("ComparisonListController", __webpack_require__(12));


/***/ },
/* 11 */
/***/ function(module, exports) {

	module.exports = function ($scope) {

	};



/***/ },
/* 12 */
/***/ function(module, exports) {

	module.exports = function ($scope) {

	};



/***/ }
]);