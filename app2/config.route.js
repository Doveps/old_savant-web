angular
    .module('app')
    .config(routeConfig);

function routeConfig($stateProvider) {
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
            templateUrl: "app/comparisons.html",
        })
        .state('dashboard.comparison', {
            url: "comparisons/:id",
            templateUrl: "app/comparison.html",
        })
        .state('dashboard.sets', {
            url: "sets",
            templateUrl: "app/sets.html",
        })
        .state('dashboard.set', {
            url: "sets/:id",
            templateUrl: "app/set.html",
        })
}
