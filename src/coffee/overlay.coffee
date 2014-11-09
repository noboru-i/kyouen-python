$ = jQuery
$.fn.extend
  overlay: (overlayConfig) ->
    $target = $(this)
    defaultOption =
      position: "fixed"
      bottom: 0
      left: 0
      right: 0
      top: 0
      backgroundColor: "rgba(0, 0, 0, 0.5)"

    option = $.extend(defaultOption, overlayConfig)
    $overlay = $("#overlay_area")
    unless $overlay.length
      # 存在しない場合は作成
      $overlay = $("<div />").attr(id: "overlay_area")
      $("body").append $overlay

    $overlay.css option
    $overlay.append $target
    $overlay.click ->
      # オーバレイ領域がクリックされた場合は隠す
      $overlay.hide()
      $target.hide()

    $target.click (e) ->
      # ターゲット領域がクリックされた場合はイベントの伝達を止める
      e.stopPropagation()

    $overlay.show()
    $target.show()
