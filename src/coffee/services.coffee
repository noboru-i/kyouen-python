'use strict'

@KyouenApp.factory 'recentService', ['$http', ($http) ->
  new class RecentService
    constructor: ->

    fetch: ()->
      $http.get('/api/recent').then (response) ->
        response.data
]
