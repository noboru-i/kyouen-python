'use strict'

RecentStagesController = ($scope, recentService) ->
  $scope.init = ->
    $scope.recents = recentService.fetch()
@KyouenApp
.controller('RecentStagesController', ['$scope', 'recentService', RecentStagesController])
