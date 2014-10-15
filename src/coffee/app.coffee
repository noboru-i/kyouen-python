'use strict'

KyouenApp = angular.module('kyouenApp', ['ngRoute'], ($routeProvider)->
  $routeProvider.when('/html/list.html',{ controller: 'ListController', templateUrl: 'html/list.html'})
)

ListController = ($scope) ->
  $scope.title = "Sample 1"
KyouenApp.controller('ListController', ListController);
