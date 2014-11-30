'use strict'

@KyouenApp
.filter 'listLink', () ->
  (stageNo)->
    pageNo = Math.floor((stageNo - 1) / 10) + 1
    "/html/list.html?page_no=#{pageNo}&open=#{stageNo}"
.filter 'jst', ['$filter', ($filter) ->
  (date)->
    dateFilter = $filter 'date'
    offset = new Date().getTimezoneOffset() * 60 * 1000
    dateFilter (Date.parse(date) - offset), 'yyyy/MM/dd HH:mm'
]