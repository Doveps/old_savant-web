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
