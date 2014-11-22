'use strict'

@KyouenApp
.factory 'recentStagesService', ['$http', ($http) ->
  new class RecentStagesService
    constructor: ->

    fetch: ()->
      $http.get('/api/recent_stages').then (response) ->
        response.data
]
.factory 'activityService', ['$http', ($http) ->
  new class ActivityService
    constructor: ->

    fetch: ()->
      $http.get('/api/activities').then (response) ->
        response.data
]
.factory 'loginService', ['$http', ($http) ->
  new class LoginService
    constructor: ->

    fetch: ()->
      $http.get('/api/login').then (response) ->
        response.data
]
.factory 'stageCountService', ['$http', ($http) ->
  new class StageCountService
    constructor: ->

    fetch: ()->
      $http.get('/api/stages/count').then (response) ->
        response.data
]
.factory 'stageService', ['$http', ($http) ->
  new class StageService
    constructor: ->

    fetch: (pageNo)->
      $http({
          url: '/api/stages'
          method: "GET",
          params: {page_no: pageNo}
          }).then (response) ->
        response.data
]
.factory 'rankingService', ['$http', ($http) ->
  new class rankingService
    constructor: ->

    fetch: ()->
      $http({
          url: '/api/rankings'
          method: 'GET'
          }).then (response) ->
        response.data
]