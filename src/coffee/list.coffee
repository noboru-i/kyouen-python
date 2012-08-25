# 共円領域の描画
drawKyouen = (canvas, kyouen) ->
  width = canvas.width
  stoneSize = getStoneSize(kyouen.size, width)

  ctx = canvas.getContext("2d")
  ctx.clearRect 0, 0, width, width
  ctx.strokeStyle = "rgb(38, 38, 38)"
  ctx.lineWidth = 2
  ctx.fillStyle = "rgb(0, 218, 0)"
  ctx.fillRect 0, 0, stoneSize * 2 * kyouen.size, stoneSize * 2 * kyouen.size
  ctx.strokeRect 0, 0, stoneSize * 2 * kyouen.size, stoneSize * 2 * kyouen.size
  drawBackground ctx, kyouen.size, stoneSize
  drawStone ctx, kyouen.stage, kyouen.size, stoneSize

# クリア状態の描画
drawClear = (canvas, kyouen) ->
  return  if kyouen.clear isnt "1"
  $div = $(canvas).parent().attr("title", "クリア済み")
  $div.children(".stageno").addClass "clear"

# 石のサイズを返す
getStoneSize = (size, width) ->
  stoneSize = Math.floor(width / size / 2)
  stoneSize -= width % size
  stoneSize

# 背景の描画
drawBackground = (ctx, size, stoneSize) ->
  for i in [0..size]
    ctx.beginPath()
    ctx.moveTo stoneSize * 2 * (i + 0.5), 0
    ctx.lineTo stoneSize * 2 * (i + 0.5), stoneSize * 2 * size
    ctx.closePath()
    ctx.stroke()
    ctx.beginPath()
    ctx.moveTo 0, stoneSize * 2 * (i + 0.5)
    ctx.lineTo stoneSize * 2 * size, stoneSize * 2 * (i + 0.5)
    ctx.closePath()
    ctx.stroke()

drawStone = (ctx, stage, size, stoneSize) ->
  for i in [0..size]
    for j in [0..size]
      index = i * size + j
      c = stage.charAt(index)
      if c is "0"
        continue
      if c is "1"
        ctx.fillStyle = "rgb(25, 25, 25)"
      else ctx.fillStyle = "rgb(252, 252, 252)"  if c is "2"
      ctx.beginPath()
      ctx.arc stoneSize * 2 * (j + 0.5), stoneSize * 2 * (i + 0.5), stoneSize, 0, Math.PI * 2, false
      ctx.fill()
      ctx.closePath()

drawKyouenData = (ctx, kyouenData, stoneSize, size) ->
  ctx.lineWidth = 5
  ctx.beginPath()

  if kyouenData.isLine
    
    # 直線の場合
    line = kyouenData.line
    startX = 0
    startY = 0
    stopX = 0
    stopY = 0
    maxScrnWidth = stoneSize * 2 * size
    if line.a is 0
      
      # x軸と平行な場合
      startX = 0
      startY = line.getY(0) * stoneSize * 2 + stoneSize
      stopX = maxScrnWidth
      stopY = line.getY(0) * stoneSize * 2 + stoneSize
    else if line.b is 0
      
      # y軸と平行な場合
      startX = line.getX(0) * stoneSize * 2 + stoneSize
      startY = 0
      stopX = line.getX(0) * stoneSize * 2 + stoneSize
      stopY = maxScrnWidth
    else
      
      # 上記以外の場合
      if -1 * line.c / line.b > 0
        startX = 0
        startY = line.getY(-0.5) * stoneSize * 2 + stoneSize
        stopX = maxScrnWidth
        stopY = line.getY(size - 0.5) * stoneSize * 2 + stoneSize
      else
        startX = line.getX(-0.5) * stoneSize * 2 + stoneSize
        startY = 0
        stopX = line.getX(size - 0.5) * stoneSize * 2 + stoneSize
        stopY = maxScrnWidth
    ctx.moveTo startX, startY
    ctx.lineTo stopX, stopY
    ctx.closePath()
  else
    
    # 円の場合
    # 円の場合
    cx = kyouenData.center.x * stoneSize * 2 + stoneSize
    cy = kyouenData.center.y * stoneSize * 2 + stoneSize
    radius = kyouenData.radius * stoneSize * 2
    ctx.arc cx, cy, radius, 0, Math.PI * 2, false
  ctx.stroke()

createPlayableKyouen = (canvas) ->
  k = new Kyouen(canvas)
  
  # 表示領域の高さ・幅のうち、最小のものの8割をcanvasのサイズとする
  canvasSize = Math.floor(Math.min(document.body.clientWidth, document.body.clientHeight, document.documentElement.clientWidth, document.documentElement.clientHeight) * 0.8)
  canvasSize -= canvasSize % (k.size * 2) # 端数を調整
  $kyouenView = $("#kyouenView")

  unless $kyouenView.length
    # 存在しない場合、作成
    createKyouenView()
    $kyouenView = $("#kyouenView")

  $kyouenView.overlay()
  $stageNo = $("#stageno0")
  $creator = $("#creator0")
  $canvas = $("#canvas0")
  $button = $("#kyouenButton")
  $dialog = $("#dialog")
  $stageNo.html k.stageNo
  $creator.html k.creator
  $kyouenView.css
    width: (canvasSize + 50) + "px"
    height: (canvasSize + 120) + "px"

  $canvas.attr
    width: canvasSize + "px"
    height: canvasSize + "px"
    "data-stageno": k.stageNo
    "data-stage": k.stage
    "data-size": k.size

  $button.css width: Math.floor(canvasSize * 0.8) + "px"
  $button.disableButton()
  
  # イベントを設定
  kyouen = new Kyouen($canvas[0])
  $kyouenView.unbind "click"
  $kyouenView.click (e) ->
    e.stopPropagation()

  $canvas.unbind "click"
  $canvas.click (e) ->
    $dialog = $("#dialog")
    $dialog.remove()  if $dialog.length
    position = adjust(e, kyouen)
    kyouen.select position.x, position.y
    positions = kyouen.getSelectedStonePositions()
    if positions.length is 4
      $button.enableButton()
    else
      $button.disableButton()

  $button.unbind "click"
  $button.click (e) ->
    kyouenData = kyouen.isKyouenSelected()
    console.log kyouenData
    $button.disableButton()
    if kyouenData?
      $canvas.unbind "click"
      ctx = $canvas[0].getContext("2d")
      stoneSize = getStoneSize(kyouen.size, $canvas[0].width)
      drawKyouenData ctx, kyouenData, stoneSize, kyouen.size
      $.post "/page/add",
        stageNo: kyouen.stageNo

      $(k.canvas).attr "data-clear": "1"
      kyouen.clear = "1"
      drawClear $("#canvas" + kyouen.stageNo)[0], kyouen
      $stageNo.addClass "clear"
      showDialog "共円！！"
    else
      
      # 未選択状態に戻す
      kyouen.stage = kyouen.stage.replace(/2/g, "1")
      drawKyouen $canvas[0], kyouen
      showDialog "共円ではありません。"

  $dialog.remove()
  
  # 共円を描画
  drawKyouen $canvas[0], k
  if k.clear is "1"
    $stageNo.addClass "clear"
  else
    $stageNo.removeClass "clear"
  
  # 共円領域を表示
  $kyouenView.show()
showDialog = (message) ->
  dialogWidth = $("#kyouenView").width() - 10
  dialogHeight = 100
  $dialog = $("#dialog")
  $dialogMessage = $("#dialogMessage")
  unless $dialog.length
    $dialog = $("<div />").attr(id: "dialog")
    $dialog.appendTo $("#kyouenView")
    $dialogMessage = $("<div />").attr(id: "dialogMessage").css(lineHeight: dialogHeight + "px").html(message)
    $dialogMessage.appendTo $dialog
  $dialog.css
    width: dialogWidth + "px"
    height: dialogHeight + "px"
    marginTop: -dialogHeight / 2 + "px"
    marginLeft: -dialogWidth / 2 + "px"
    display: "none"

  $dialogMessage.html message
  $dialog.click (e) ->
    $dialog.remove()

  $dialog.hover ()->
    $dialog.stop().animate {
        backgroundColor: "#fff"
        color: "#004C9A"
      }
    , 200
    $dialog.css textDecoration: "underline"
  , ()->
    $dialog.stop().animate {
        backgroundColor: "#eee"
        color: "#333"
      }
    , 200
    $dialog.css textDecoration: "none"

  $dialog.show 200
removeDialog = ->
  $dialog = $("#dialog")
  return  unless $dialog
  $dialog.remove()
createKyouenView = ->
  $kyouenView = $("<div />").attr(id: "kyouenView")
  $kyouenView.appendTo $("body")
  $stageNo = $("<div />").attr(id: "stageno0")
  $stageNo.appendTo $kyouenView
  $creator = $("<div />").attr(id: "creator0")
  $creator.appendTo $kyouenView
  $canvas = $("<canvas />").attr(id: "canvas0")
  $canvas.appendTo $kyouenView
  $button = $("<input />").attr(
    id: "kyouenButton"
    type: "button"
    value: "共円！！"
  )
  $button.appendTo $kyouenView

# 石の位置(x座標,y座標)を返す
adjust = (e, kyouen) ->
  clientRect = e.target.getBoundingClientRect()
  size = kyouen.size
  stoneSize = getStoneSize(size, e.target.width)
  canvasX = e.clientX - clientRect.left
  canvasY = e.clientY - clientRect.top
  pos = {}
  pos.x = Math.ceil(canvasX / stoneSize / 2) - 1
  pos.y = Math.ceil(canvasY / stoneSize / 2) - 1
  return pos

$ = jQuery
$.fn.extend
  kyouenView: (config) ->
    canvas = $(this)
    for c in canvas
      k = new Kyouen(c)
      drawKyouen c, k
      drawClear c, k
    return this

  overlayKyouen: (config) ->
    targets = this
    targets.click ->
      createPlayableKyouen $("canvas", this)[0]

  createPlayableKyouen: (config) ->
    createPlayableKyouen $("canvas", this)[0]

  disableButton: (config) ->
    if @button
      @button "disable"
      @button "refresh"
    else
      @attr disabled: "disabled"
    this

  enableButton: (config) ->
    if @button
      @button "enable"
    else
      @removeAttr "disabled"
    this


# 文字列の特定の位置の文字を変更
String::replaceCharAt = (at, replaceChar) ->
  before = @substring(0, at)
  after = @slice(at + 1)
  before + replaceChar + after


# 共円クラスの定義
class Kyouen
  constructor: (canvas) ->
    @obj = this
    @canvas = canvas
    @stageNo = Number(canvas.getAttribute("data-stageno"))
    @stage = canvas.getAttribute("data-stage")
    @size = Number(canvas.getAttribute("data-size"))
    @creator = canvas.getAttribute("data-creator")
    @clear = canvas.getAttribute("data-clear")

  # XY座標をインデックスに変換
  position2Index: (x, y) ->
    x + y * @size

  
  # インデックスをXY座標に変換
  index2Position: (index) ->
    pos = new Point(index % @size, Math.floor(index / @size))
    pos

  
  # 指定された位置の石を選択
  select: (x, y) ->
    index = @position2Index(x, y)
    c = @stage.charAt(index)
    if c is "1"
      @stage = @stage.replaceCharAt(index, "2")
    else @stage = @stage.replaceCharAt(index, "1")  if c is "2"
    drawKyouen @canvas, this

  
  # 共円が選択されている場合、trueを返却
  isKyouenSelected: ->
    selectedStonePositions = @getSelectedStonePositions()
    return null  if selectedStonePositions.length < 4
    p1 = selectedStonePositions[0]
    p2 = selectedStonePositions[1]
    p3 = selectedStonePositions[2]
    p4 = selectedStonePositions[3]
    
    # p1,p2の垂直二等分線を求める
    l12 = @getMidperpendicular(p1, p2)
    
    # p2,p3の垂直二等分線を求める
    l23 = @getMidperpendicular(p2, p3)
    
    # 交点を求める
    intersection123 = @getIntersection(l12, l23)
    unless intersection123?
      
      # p1,p2,p3が直線上に存在する場合
      l34 = @getMidperpendicular(p3, p4)
      intersection234 = @getIntersection(l23, l34)

      # p2,p3,p4が直線状に存在する場合
      unless intersection234?
        return new KyouenData(p1, p2, p3, p4, true, null, null, new Line(p1, p2))
    else
      dist1 = @getDistance(p1, intersection123)
      dist2 = @getDistance(p4, intersection123)
      if Math.abs(dist1 - dist2) < 0.0000001
        return new KyouenData(p1, p2, p3, p4, false, intersection123, dist1, null)
    return null

  
  # 選択されている石の座標を返却
  getSelectedStonePositions: ->
    stoneArray = []

    for i in [0..@size*@size]
      c = @stage.charAt(i)
      stoneArray.push @index2Position(i)  if c is "2"
    stoneArray

  
  # 二点間の距離を求める
  getDistance: (p1, p2) ->
    p1.difference(p2).getAbs()

  
  # 交点を求める
  getIntersection: (l1, l2) ->
    f1 = l1.p2.x - l1.p1.x
    g1 = l1.p2.y - l1.p1.y
    f2 = l2.p2.x - l2.p1.x
    g2 = l2.p2.y - l2.p1.y
    det = f2 * g1 - f1 * g2
    return null  if det is 0
    dx = l2.p1.x - l1.p1.x
    dy = l2.p1.y - l1.p1.y
    t1 = (f2 * dy - g2 * dx) / det
    new Point(l1.p1.x + f1 * t1, l1.p1.y + g1 * t1)

  
  # 垂直二等分線を求める
  getMidperpendicular: (p1, p2) ->
    midpoint = @getMidpoint(p1, p2)
    diff = p1.difference(p2)
    gradient = new Point(diff.y, -1 * diff.x)
    new Line(midpoint, midpoint.sum(gradient))

  
  # 中点を求める
  getMidpoint: (p1, p2) ->
    midpoint = new Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)
    midpoint


# 点情報オブジェクト
class Point
  constructor: (x, y) ->
    @x = x
    @y = y

  # 和を求める
  sum: (p2) ->
    new Point(@x + p2.x, @y + p2.y)

  
  # 差を求める
  difference: (p2) ->
    new Point(@x - p2.x, @y - p2.y)

  
  # 絶対値を求める
  getAbs: ->
    Math.sqrt @x * @x + @y * @y


# 直線情報オブジェクト
class Line
  constructor: (p1, p2) ->
    @p1 = p1
    @p2 = p2
    @a = p1.y - p2.y
    @b = p2.x - p1.x
    @c = p1.x * p2.y - p2.x * p1.y

  getY: (x) ->
    y = -1 * (@a * x + @c) / @b
    y

  getX: (y) ->
    x = -1 * (@b * y + @c) / @a
    x


# 共円情報オブジェクト
class KyouenData
  constructor: (p1, p2, p3, p4, isLine, center, radius, line) ->
    @points = [p1, p2, p3, p4]
    @isLine = isLine
    @center = center
    @radius = radius
    @line = line
