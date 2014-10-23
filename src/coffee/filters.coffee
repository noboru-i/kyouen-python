'use strict'

@KyouenApp
.filter 'listLink', () ->
  (stageNo)->
    index = (stageNo - 1) - (stageNo - 1) % 10
    "/page/list.html?index=#{index}&open=#{stageNo}"
