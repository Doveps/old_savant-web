var angular = require('angular');

angular
    .module('app')
    .controller("SetDetailController", require('./set-detail'))
    .controller("SetListController", require('./sets'));
