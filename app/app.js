angular
    .module('app', [
        /*
         * Angular modules
         */
        'ngResource', 'ui.router', 'ngStorage', 'ngSanitize',

        /*
         * 3rd Party modules
         */
        'angular-loading-bar',
        'ngAnimate',
        'oc.lazyLoad',
        'ui.date',
        'LocalStorageModule',
        'ui.bootstrap',
        'infinite-scroll',

        'datatables',
        'datatables.fixedcolumns',
        'datatables.select',
        'datatables.columnfilter',
        // 'datatables.light-columnfilter',
        'angular.filter'

    ])
    .config(routeConfig)
    .run(run);

function routeConfig($urlRouterProvider, $httpProvider, $resourceProvider, cfpLoadingBarProvider) {
    // Enable cors in client side
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    // Configure loading bar
    cfpLoadingBarProvider.includeBar = false;

    $urlRouterProvider.otherwise("/login");
    $resourceProvider.defaults.stripTrailingSlashes = false;
}

function run($rootScope, $state, $stateParams) {
    $rootScope.$state = $state;
    $rootScope.$stateParams = $stateParams;
}