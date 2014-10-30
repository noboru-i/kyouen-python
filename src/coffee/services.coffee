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
