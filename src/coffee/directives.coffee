'use strict'

RecentStagesController = ($scope, recentService) ->
  $scope.init = ->
    recentService.fetch().then (data) ->
      $scope.recents = data

@KyouenApp
.directive 'recentStages', ()->
  restrict: 'E'
  replace: true
  templateUrl: 'html/parts/recent_stages.html'
  controller: ['$scope', 'recentService', RecentStagesController]
  link: (scope, element, attrs, ctrl) ->
    scope.init()
