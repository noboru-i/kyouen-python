'use strict'

@KyouenApp = angular.module('kyouenApp', [
  'ngRoute',
  'ui.bootstrap'
])

@KyouenApp.config(['$routeProvider', ($routeProvider)->
  $routeProvider.when('/html/list.html',
    controller: 'ListController'
    templateUrl: 'html/list.html'
  )
])
