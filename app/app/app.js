var angular = require('angular');

require('angular-resource');
require('angular-ui-router');


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

require('./shared');
require('./sets');
require('./comparisons');