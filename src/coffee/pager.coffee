createPager = ($pager) ->
  size = Number($pager[0].getAttribute("data-size"))
  index = Number($pager[0].getAttribute("data-index"))
  count = 10
  startIndex = 1
  lastIndex = Math.floor((size - 1) / count) + 1

  $prev = $("<div />").css(
    float: "left"
    width: "10%"
    margin: "0 auto"
  ).append("<<")
  .mouseover ->
    scroll $pager_content, -1
  .mouseout ->
    clearInterval $pager_content.data("rightScroll")

  $prev.appendTo $pager
  $pager_content = $("<div />").attr(id: "pager_content").css(
    float: "left"
    width: "80%"
    overflow: "hidden"
    margin: "0 auto"
  )
  $pager_content.appendTo $pager

  for i in [0..lastIndex-1]
    $pager_content.append "&nbsp;"
    $pager_content.append $("<a />").attr(href: "javascript:loadStage(" + ((startIndex + i - 1) * count) + ")").text(startIndex + i)
    $pager_content.append "&nbsp;"

  $next = $("<div />").css(
    float: "left"
    width: "10%"
    margin: "0 auto"
  ).append(">>").mouseover ->
    scroll $pager_content, 1
  .mouseout ->
    clearInterval $pager_content.data("rightScroll")

  $next.appendTo $pager

scroll = ($scrollTarget, direction) ->
  $scrollTarget.data "rightScroll", setInterval(->
    $scrollTarget.scrollLeft $scrollTarget.scrollLeft() + direction * 5
  , 20)

$ = jQuery
$.fn.extend
  pager: (config) ->
    for p in $(this)
      createPager $(p)

$ ->
  $(".pager").pager()

