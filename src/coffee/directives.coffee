'use strict'

RecentStagesController = ($scope, recentStagesService) ->
  $scope.init = ->
    recentStagesService.fetch().then (data) ->
      $scope.recentStages = data

ActivitiesController = ($scope, activityService) ->
  $scope.init = ->
    activityService.fetch().then (data) ->
      $scope.activities = data;

LoginController = ($scope, loginService) ->
  $scope.init = ->
    loginService.fetch().then (data) ->
      $scope.currentUser = data;

@KyouenApp
.directive 'recentStages', ()->
  restrict: 'E'
  replace: true
  templateUrl: 'html/parts/recent_stages.html'
  controller: ['$scope', 'recentStagesService', RecentStagesController]
  link: (scope, element, attrs, ctrl) ->
    scope.init()

.directive 'activities', ()->
  restrict: 'E'
  replace: false
  templateUrl: 'html/parts/activities.html'
  controller: ['$scope', 'activityService', ActivitiesController]
  link: (scope, element, attrs, ctrl) ->
    scope.init()

.directive 'loginHeader', () ->
  restrict: 'E'
  replace: true
  templateUrl: 'html/parts/login_header.html'
  controller: ['$scope', 'loginService', LoginController]
  link: (scope, element, attrs, ctrl) ->
    scope.init()
