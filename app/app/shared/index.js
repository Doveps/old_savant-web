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