'use strict'

RecentStagesController = ($scope, recentService) ->
  $scope.init = ->
    $scope.recents = recentService.fetch()

@KyouenApp
.directive 'recentStages', ()->
  restrict: 'E'
  replace: true
  templateUrl: 'html/parts/recent_stages.html'
  controller: ['$scope', 'recentService', RecentStagesController]
  link: (scope, element, attrs, ctrl) ->
    scope.init()
