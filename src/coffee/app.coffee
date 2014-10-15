'use strict'

KyouenApp = angular.module('kyouenApp', ['ngRoute'], ($routeProvider)->
  $routeProvider.when('/html/list.html',
    { controller: 'ListController', templateUrl: 'html/list.html'})
)
