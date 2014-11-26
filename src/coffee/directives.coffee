'use strict'

RecentStagesController = ($scope, recentStagesService) ->
  $scope.init = ->
    recentStagesService.fetch().then (data) ->
      $scope.recentStages = data

ActivitiesController = ($scope, activityService) ->
  $scope.init = ->
    activityService.fetch().then (data) ->
      $scope.activities = data

LoginController = ($scope, loginService) ->
  $scope.init = ->
    loginService.fetch().then (data) ->
      $scope.currentUser = data

StagesPaginationController = ($scope,
    $rootScope,
    stageCountService) ->
  $scope.init = ->
    $scope.currentPage = 1
    $scope.maxSize = 10
    stageCountService.fetch().then (data) ->
      $scope.totalItems = data.count
      $scope.pageChanged(1)
  $scope.pageChanged = ->
    $rootScope.$broadcast('changeStage', $scope.currentPage)

StagesController = ($scope, $rootScope, $document, stageService) ->
  $scope.init = ->
    $rootScope.$on('changeStage', (event, stageNo)->
      stageService.fetch($scope.currentPage).then (data) ->
        $scope.stages = data
      )
  $scope.openKyouen = (kyouenInfo)->
    $rootScope.$broadcast('openKyouen', kyouenInfo)

PlayableKyouenViewController = ($scope, $rootScope) ->
  $scope.init = (canvas)->
    $scope.opend = false
    $rootScope.$on('openKyouen', (event, kyouenInfo) ->
      $scope.opend = true
      c = openKyouen(canvas, kyouenInfo)
      view = new TumeKyouenView($(c), new KyouenModel(kyouenInfo))
      view.drawKyouen()
      view.drawClear()
    )

CreateKyouenViewController = ($scope) ->
  $scope.selectedSize = 6
  $scope.sizeOptions = {
    '6x6': 6
    '9x9': 9
  }
  $scope.init = (canvas) ->
    $scope.disabledReset = true
    $scope.v = new CreateKyouenView(
      canvas: $(canvas)
      model: new KyouenModel({
        'stage': '000000000000000000000000000000000000'
        'size' : '6'
        })
      onChange: (model) ->
        if model.hasStone('1')
          $scope.$apply () ->
            $scope.disabledReset = false
      )
    $scope.v.drawKyouen()
  $scope.changeSelect = () ->
    $scope.v.model.size = $scope.selectedSize
    $scope.v.reset()
  $scope.reset = () ->
    $scope.v.reset()

RankingController = ($scope, rankingService) ->
  $scope.init = ->
    rankingService.fetch().then (data) ->
      $scope.rankings = data

@KyouenApp
.controller 'StagesPaginationController',
    ['$scope', 'recentStagesService', StagesPaginationController]

@KyouenApp
.directive 'recentStages', ()->
  restrict: 'E'
  replace: true
  templateUrl: '/html/parts/recent_stages.html'
  controller: ['$scope', 'recentStagesService', RecentStagesController]
  link: (scope, element, attrs, ctrl) ->
    scope.init()

.directive 'activities', ()->
  restrict: 'E'
  replace: false
  templateUrl: '/html/parts/activities.html'
  controller: ['$scope', 'activityService', ActivitiesController]
  link: (scope, element, attrs, ctrl) ->
    scope.init()

.directive 'loginHeader', () ->
  restrict: 'E'
  replace: true
  templateUrl: '/html/parts/login_header.html'
  controller: ['$scope', 'loginService', LoginController]
  link: (scope, element, attrs, ctrl) ->
    scope.init()

.directive 'stagePager', () ->
  restrict: 'E'
  replace: true
  templateUrl: '/html/parts/stage_pager.html'
  controller: ['$scope',
      '$rootScope',
      'stageCountService'
      StagesPaginationController]
  link: (scope, element, attrs, ctrl) ->
    scope.init()

.directive 'stages', () ->
  restrict: 'E'
  replace: true
  templateUrl: '/html/parts/stages.html'
  controller: ['$scope',
      '$rootScope',
      '$document',
      'stageService',
      StagesController]
  link: (scope, element, attrs, ctrl) ->
    scope.init()

.directive 'kyouenView', () ->
  restrict: 'E'
  replace: true
  scope: {
    stageInfo: '='
  }
  templateUrl: '/html/parts/kyouen_view.html'
  link: (scope, element, attrs) ->
    v = new KyouenView($(element),
      new KyouenModel(scope.stageInfo))
    v.drawKyouen()
    v.drawClear()

.directive 'playableKyouenView', () ->
  restrict: 'E'
  replace: true
  templateUrl: '/html/parts/playable_kyouen_view.html'
  controller: ['$scope',
      '$rootScope',
      PlayableKyouenViewController]
  link: (scope, element, attrs) ->
    scope.init(element.find('canvas'))

.directive 'createKyouenView', () ->
  restrict: 'E'
  replace: true
  templateUrl: '/html/parts/create_kyouen_view.html'
  controller: ['$scope',
      '$rootScope',
      CreateKyouenViewController]
  link: (scope, element, attrs) ->
    scope.init(element.find('canvas'))

.directive 'ranking', () ->
  restrict: 'E'
  replace: true
  templateUrl: '/html/parts/ranking.html'
  controller: ['$scope',
      'rankingService',
      RankingController]
  link: (scope, element, attrs) ->
    scope.init()
