'use strict'

@KyouenApp.factory 'recentService', ['$http', ($http) ->
  new class RecentService
    constructor: ->

    fetch: ()->
      [
        {
          stageNo: 2
          size: 6
          stage: '000000000000000000000000000000000000'
          creator: 'noboru2'
          registDate: '2014-01-02 01:02:03'
        }
        {
          stageNo: 1
          size: 6
          stage: '000000000000000000000000000000000000'
          creator: 'noboru'
          registDate: '2014-01-01 01:02:03'
        }
      ]
]
