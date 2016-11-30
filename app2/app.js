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
    .run(run);

function routeConfig($urlRouterProvider, $httpProvider, $resourceProvider) {
    // Enable cors in client side
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    $urlRouterProvider.otherwise("/");
    $resourceProvider.defaults.stripTrailingSlashes = false;
}

function run($rootScope, $state, $stateParams) {
    $rootScope.$state = $state;
    $rootScope.$stateParams = $stateParams;
}