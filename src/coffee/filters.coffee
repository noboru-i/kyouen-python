'use strict'

@KyouenApp
.filter 'listLink', () ->
  (stageNo)->
    index = (stageNo - 1) - (stageNo - 1) % 10
    "/page/list.html?index=#{index}&open=#{stageNo}"
.filter 'jst', ['$filter', ($filter) ->
  (date)->
    dateFilter = $filter 'date'
    offset = new Date().getTimezoneOffset() * 60 * 1000
    dateFilter (Date.parse(date) - offset), 'yyyy/MM/dd HH:mm'
]