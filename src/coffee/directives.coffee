'use strict'

RecentStagesController = ($scope, recentStagesService) ->
  recentStagesService.fetch().then (data) ->
    $scope.recentStages = data

ActivitiesController = ($scope, activityService) ->
  activityService.fetch().then (data) ->
    $scope.activities = data

LoginController = ($scope, loginService) ->
  loginService.fetch().then (data) ->
    $scope.currentUser = data

NavigationController = ($scope, $location) ->
  $scope.isCollapsed = true
  $scope.isActive = (pageName) ->
    $location.path().indexOf(pageName) >= 0

StagesPaginationController = ($scope,
    $rootScope,
    $location,
    stageCountService) ->
  $scope.maxSize = 10
  stageCountService.fetch().then (data) ->
    $scope.currentPage = $location.search()['page_no'] || 1
    $scope.totalItems = data.count
    $scope.pageChanged()
  $scope.pageChanged = ->
    $rootScope.$broadcast('changeStage', $scope.currentPage)

StagesController = ($scope, $rootScope, $location, stageService) ->
  $rootScope.$on('changeStage', (event, stageNo)->
    stageService.fetch(stageNo).then (data) ->
      $scope.stages = data
      open = $location.search()['open']
      if open
        index = ((open - 1) % 10)
        $scope.openKyouen(data[index])
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
      # クリックするまで表示されないバグ対応
      setTimeout () ->
        $(canvas).click()
    )

CreateKyouenViewController = ($scope) ->
  $scope.selectedSize = 6
  $scope.sizeOptions = {
    '6x6': 6
    '9x9': 9
  }
  $scope.name = ''
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
  $scope.send = () ->
    name = $scope.name
    if name.length == 0
      alert '名前を入力してください。'
      return
    $scope.v.model.creator = name
    $scope.v.model.sendStage()
    $scope.v.hideDialog()
    ''

RankingController = ($scope, rankingService) ->
  rankingService.fetch().then (data) ->
    $scope.rankings = data

@KyouenApp
.controller 'StagesPaginationController',
    ['$scope', 'recentStagesService', StagesPaginationController]

@KyouenApp
.directive 'navigation', ()->
  restrict: 'E'
  replace: true
  templateUrl: '/html/parts/navigation.html'
  controller: ['$scope', '$location', NavigationController]

.directive 'recentStages', ()->
  restrict: 'E'
  replace: true
  templateUrl: '/html/parts/recent_stages.html'
  controller: ['$scope', 'recentStagesService', RecentStagesController]

.directive 'activities', ()->
  restrict: 'E'
  replace: false
  templateUrl: '/html/parts/activities.html'
  controller: ['$scope', 'activityService', ActivitiesController]

.directive 'loginHeader', () ->
  restrict: 'E'
  replace: true
  templateUrl: '/html/parts/login_header.html'
  controller: ['$scope', 'loginService', LoginController]

.directive 'stagePager', () ->
  restrict: 'E'
  replace: true
  templateUrl: '/html/parts/stage_pager.html'
  controller: ['$scope',
      '$rootScope',
      '$location',
      'stageCountService'
      StagesPaginationController]

.directive 'stages', () ->
  restrict: 'E'
  replace: true
  templateUrl: '/html/parts/stages.html'
  controller: ['$scope',
      '$rootScope',
      '$location',
      'stageService',
      StagesController]

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
