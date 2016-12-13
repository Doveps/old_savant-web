var angular = require('angular');

angular
    .module('app')
    .controller("ComparisonDetailController", require('./comparison-detail'))
    .controller("ComparisonListController", require('./comparisons'));
