# 文字列の特定の位置の文字を変更
String::replaceCharAt = (at, replaceChar) ->
  before = @substring(0, at)
  after = @slice(at + 1)
  before + replaceChar + after

# 共円表示用クラス
class @KyouenView
  # コンストラクタ
  # @canvas canvasエレメント
  # @model KyouenModelオブジェクト
  constructor: (@canvas, @model) ->
    @init()

  # 初期化処理を行う
  init: ->

  # 共円領域の描画
  drawKyouen: ->
    ctx = @canvas[0].getContext("2d")
    @drawBackground ctx
    @drawStones ctx

  # クリア状態の描画
  drawClear: ->
    if @model.clear isnt "1"
      return
    $div = @canvas.parent().attr("title", "クリア済み")
    $div.children(".stageno").addClass("clear")

  # 石のサイズを返す
  getStoneSize: ->
    size = @model.size
    width = @canvas.width()
    stoneSize = Math.floor(width / size / 2)
    stoneSize -= width % size
    return stoneSize

  # 背景の描画
  drawBackground: (ctx) ->
    size = @model.size
    width = @canvas.width()
    stoneSize = @getStoneSize()

    ctx.clearRect 0, 0, width, width
    ctx.strokeStyle = "rgb(38, 38, 38)"
    ctx.lineWidth = 2
    ctx.fillStyle = "rgb(0, 218, 0)"
    ctx.fillRect 0, 0, stoneSize * 2 * size, stoneSize * 2 * size
    ctx.strokeRect 0, 0, stoneSize * 2 * size, stoneSize * 2 * size

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

  # 石の描画
  drawStones: (ctx) ->
    stage = @model.stage
    size = @model.size
    stoneSize = @getStoneSize()
    for i in [0..size]
      for j in [0..size]
        index = i * size + j
        c = stage.charAt(index)
        switch c
          when "0"
            continue
          when "1"
            ctx.fillStyle = "rgb(25, 25, 25)"
          when "2"
            ctx.fillStyle = "rgb(252, 252, 252)"
        ctx.beginPath()
        ctx.arc stoneSize * 2 * (j + 0.5), stoneSize * 2 * (i + 0.5), stoneSize, 0, Math.PI * 2, false
        ctx.fill()
        ctx.closePath()

  # 共円を表す直線・円を描画
  drawKyouenData: (ctx, kyouenData) ->
    size = @model.size
    stoneSize = @getStoneSize()
    ctx.lineWidth = 5
    ctx.beginPath()
    ctx.strokeStyle = "rgb(252, 0, 0)"

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
      cx = kyouenData.center.x * stoneSize * 2 + stoneSize
      cy = kyouenData.center.y * stoneSize * 2 + stoneSize
      radius = kyouenData.radius * stoneSize * 2
      ctx.arc cx, cy, radius, 0, Math.PI * 2, false
    ctx.stroke()

  # 石の位置(x座標,y座標)を返す
  adjust: (e, kyouen) ->
    clientRect = e.target.getBoundingClientRect()
    size = kyouen.size
    stoneSize = @getStoneSize()
    canvasX = e.clientX - clientRect.left
    canvasY = e.clientY - clientRect.top
    pos = {}
    pos.x = Math.ceil(canvasX / stoneSize / 2) - 1
    pos.y = Math.ceil(canvasY / stoneSize / 2) - 1
    return pos

  # ダイアログの表示
  showDialog: (message) ->
    $dialog = $("#dialog")
    dialogWidth = $dialog.width()
    dialogHeight = $dialog.height()
    $dialog.css
      width: dialogWidth + "px"
      height: dialogHeight + "px"
      marginTop: -dialogHeight / 2 + "px"
      marginLeft: -dialogWidth / 2 + "px"
      display: "none"

    $dialogMessage = $("#dialogMessage")
    $dialogMessage.html message
    $dialog.click (e) =>
      if e.target.id is "dialogMessage"
        @hideDialog()

    $dialog.hover ()->
      $dialog.stop().animate {
          backgroundColor: "#fff"
          color: "#004C9A"
        }
      , 200
    , ()->
      $dialog.stop().animate {
          backgroundColor: "#eee"
          color: "#333"
        }
      , 200
    $dialog.show 200

  # ダイアログの削除
  hideDialog: ->
    $("#dialog")?.hide();


# 詰め共円領域の作成
@openKyouen = (canvas, kyouenInfo) ->
  model = new KyouenModel(kyouenInfo)
  # 表示領域の高さ・幅のうち、最小のものの8割をcanvasのサイズとする
  canvasSize = Math.floor((Math.min(document.body.clientWidth, document.body.clientHeight, document.documentElement.clientWidth, document.documentElement.clientHeight) - 100) * 0.8)
  canvasSize -= canvasSize % (model.size * 2) # 端数を調整
  $kyouenView = $("#kyouenView")

  $kyouenView.overlay()
  $stageNo = $("#stageno0")
  $creator = $("#creator0")
  $canvas = $("#canvas0")
  $button = $("#kyouenButton")
  $dialog = $("#dialog")
  $stageNo.text model.stageNo
  $creator.text model.creator
  $kyouenView.css
    width: (canvasSize + 50) + "px"
    height: (canvasSize + 120) + "px"

  $canvas.attr
    width: canvasSize + "px"
    height: canvasSize + "px"
    "class": "kyouenView"

  $button.css
    width: Math.floor(canvasSize * 0.8) + "px"
  $button.disableButton()

  $kyouenView.unbind "click"
  $kyouenView.click (e) ->
    e.stopPropagation()

  return $canvas[0]

# 共円作成用クラス
class CreateKyouenView extends KyouenView
  constructor: (@config) ->
    super(@config.canvas, @config.model)
    @init()

  init: () ->
    super()
    @canvas.unbind "click"
    @canvas.click (e) =>
      @hideDialog()
      position = @adjust(e, @model)
      @model.put position.x, position.y
      @drawKyouen()
      positions = @model.getSelectedStonePositions('1')
      if positions.length >= 4
        kyouenData = @model.isKyouenSelected('1')
        if kyouenData?
          # 共円が発生
          for p in kyouenData.points
            index = @model.position2Index p.x, p.y
            @model.stage = @model.stage.replaceCharAt index, '2'
            @drawKyouen()
          ctx = @canvas[0].getContext("2d")
          @drawKyouenData ctx, kyouenData
          @showDialog "共円！！"
          @canvas.unbind "click"
          @config.onKyouen? @model
      @config.onChange? @model

  reset: () ->
    @hideDialog()
    @model.resetStage()
    @init()
    @drawKyouen()

# 詰め共円用クラス
class @TumeKyouenView extends KyouenView
  constructor: (@canvas, @model) ->
    super(@canvas, @model)
    @init()

  init: () ->
    super()
    @hideDialog()
    # イベントを設定
    $button = $("#kyouenButton")
    $dialog = $("#dialog")

    @canvas.unbind "click"
    @canvas.click (e) =>
      @hideDialog()
      position = @adjust(e, @model)
      @model.select position.x, position.y
      @drawKyouen()
      positions = @model.getSelectedStonePositions()
      if positions.length is 4
        $button.enableButton()
      else
        $button.disableButton()

    $button.unbind "click"
    $button.click (e) =>
      return if not $button.isEnableButton()
      kyouenData = @model.isKyouenSelected()
      $button.disableButton()
      if kyouenData?
        # 共円の場合
        @canvas.unbind "click"
        ctx = @canvas[0].getContext("2d")
        @drawKyouenData ctx, kyouenData
        $.post "/page/add",
          stageNo: @model.stageNo

        $(@model.canvas).attr "data-clear": "1"
        @model.clear = "1"
        # 親canvasにクリア情報を付ける
        parentCanvas = $("#canvas" + @model.stageNo)
        if parentCanvas[0]?
          parentView = new KyouenView(parentCanvas, @model)
          parentView.drawClear()
        $stageNo = $("#stageno0")
        $stageNo.addClass "clear"
        @showDialog "共円！！"
      else
        # 未選択状態に戻す
        @model.stage = @model.stage.replace(/2/g, "1")
        @drawKyouen()
        @showDialog "共円ではありません。"

  # 共円領域の描画
  drawKyouen: () ->
    super()
    $stageNo = $("#stageno0")
    if @model.clear is "1"
      $stageNo.addClass "clear"
    else
      $stageNo.removeClass "clear"

# 共円クラスの定義
class @KyouenModel
  constructor: (stageInfo) ->
    @stageNo = stageInfo.stageNo
    @stage = stageInfo.stage
    @size = stageInfo.size
    @creator = stageInfo.creator
    @clear = stageInfo.clear

  # XY座標をインデックスに変換
  position2Index: (x, y) ->
    return x + y * @size

  # インデックスをXY座標に変換
  index2Position: (index) ->
    return new Point(index % @size, Math.floor(index / @size))

  # 指定された位置の石を選択
  select: (x, y) ->
    index = @position2Index(x, y)
    c = @stage.charAt(index)
    if c is "1"
      @stage = @stage.replaceCharAt(index, "2")
    else if c is "2"
      @stage = @stage.replaceCharAt(index, "1")

  # 指定された位置に石を設定
  put: (x, y) ->
    index = @position2Index(x, y)
    c = @stage.charAt(index)
    if c is "0"
      @stage = @stage.replaceCharAt(index, "1")

  # 共円が選択されている場合、trueを返却
  isKyouenSelected: (stone = "2")->
    selectedStonePositions = @getSelectedStonePositions(stone)
    if selectedStonePositions.length < 4
      return null
    for i in [0..(selectedStonePositions.length-4)]
      p1 = selectedStonePositions[i];
      for j in [(i+1)..(selectedStonePositions.length-3)]
        p2 = selectedStonePositions[j];
        for k in [(j+1)..(selectedStonePositions.length-2)]
          p3 = selectedStonePositions[k];
          for l in [(k+1)..(selectedStonePositions.length-1)]
            p4 = selectedStonePositions[l];
            data = @isKyouen p1, p2, p3, p4
            if data != null
              return data

  isKyouen: (p1, p2, p3, p4) ->
    # p1,p2の垂直二等分線を求める
    l12 = p1.getMidperpendicular(p2)

    # p2,p3の垂直二等分線を求める
    l23 = p2.getMidperpendicular(p3)

    # 交点を求める
    intersection123 = @getIntersection(l12, l23)
    unless intersection123?
      # p1,p2,p3が直線上に存在する場合
      l34 = p3.getMidperpendicular(p4)
      intersection234 = @getIntersection(l23, l34)

      unless intersection234?
        # p2,p3,p4が直線状に存在する場合
        return new KyouenData(p1, p2, p3, p4, true, null, null, new Line(p1, p2))
    else
      dist1 = p1.getDistance(intersection123)
      dist2 = p4.getDistance(intersection123)
      if Math.abs(dist1 - dist2) < 0.0000001
        return new KyouenData(p1, p2, p3, p4, false, intersection123, dist1, null)
    return null

  # 選択されている石の座標を返却
  getSelectedStonePositions: (stone = "2")->
    stoneArray = []
    for i in [0..@size*@size]
      c = @stage.charAt(i)
      if c is stone
        stoneArray.push @index2Position(i)
    return stoneArray

  # 交点を求める
  getIntersection: (l1, l2) ->
    f1 = l1.p2.x - l1.p1.x
    g1 = l1.p2.y - l1.p1.y
    f2 = l2.p2.x - l2.p1.x
    g2 = l2.p2.y - l2.p1.y
    det = f2 * g1 - f1 * g2
    if det is 0
      return null
    dx = l2.p1.x - l1.p1.x
    dy = l2.p1.y - l1.p1.y
    t1 = (f2 * dy - g2 * dx) / det
    return new Point(l1.p1.x + f1 * t1, l1.p1.y + g1 * t1)

  # 石が置かれているか判定する
  hasStone: (stone='1')->
    @stage.indexOf(stone) isnt -1

  # 石の配置を初期化する
  resetStage: () ->
    if @size is 6
      @stage = '000000000000000000000000000000000000'
    else
      @stage = '000000000000000000000000000000000000000000000000000000000000000000000000000000000'

  # 送信する
  sendStage: () ->
    url = '/kyouen/regist'
    tmpStage = @stage.replace /2/g, '1'
    param =
      data: [@size, tmpStage, @creator].join(',')
    callback = (data) ->
      reg = new RegExp('success stageNo=([0-9]*)');
      if not data.match reg
        if data is 'registered'
          alert '登録済みです。'
          return
        alert '送信に失敗しました。'
        return
      alert '送信しました。ステージ番号=' + data.replace reg, '$1'

    $.post url, param, callback

  # 石の数を返す
  getStoneCount: () ->
    # 0以外の文字列長を返す
    stage = @stage.replace /0/g, ''
    count = stage.length
    count

# 点情報オブジェクト
class Point
  constructor: (@x, @y) ->

  # 和を求める
  sum: (p2) ->
    return new Point(@x + p2.x, @y + p2.y)

  # 差を求める
  difference: (p2) ->
    return new Point(@x - p2.x, @y - p2.y)

  # 絶対値を求める
  getAbs: ->
    return Math.sqrt @x * @x + @y * @y

  # 二点間の距離を求める
  getDistance: (p2) ->
    return this.difference(p2).getAbs()

  # 中点を求める
  getMidpoint: (p2) ->
    return new Point((@x + p2.x) / 2, (@y + p2.y) / 2)

  # 垂直二等分線を求める
  getMidperpendicular: (p2) ->
    midpoint = this.getMidpoint(p2)
    diff = this.difference(p2)
    gradient = new Point(diff.y, -1 * diff.x)
    return new Line(midpoint, midpoint.sum(gradient))

# 直線情報オブジェクト
class Line
  constructor: (p1, p2) ->
    @p1 = p1
    @p2 = p2
    @a = p1.y - p2.y
    @b = p2.x - p1.x
    @c = p1.x * p2.y - p2.x * p1.y

  getY: (x) ->
    return -1 * (@a * x + @c) / @b

  getX: (y) ->
    return -1 * (@b * y + @c) / @a

# 共円情報オブジェクト
class KyouenData
  constructor: (p1, p2, p3, p4, isLine, center, radius, line) ->
    @points = [p1, p2, p3, p4]
    @isLine = isLine
    @center = center
    @radius = radius
    @line = line

$ = jQuery
$.fn.extend
  overlayPlayableKyouen: (config) ->
    this.click ->
      c = openKyouen $("canvas", this)[0]
      k = new KyouenModel(c)
      view = new TumeKyouenView($(c), k)
      view.drawKyouen()
      view.drawClear()
      view

  tumeKyouen: (config) ->
    c = $("canvas", this)[0]
    k = new KyouenModel(c)
    view = new TumeKyouenView($(c), k)
    view.drawKyouen()
    view.drawClear()
    view

  createKyouen: (config) ->
    c = this[0]
    k = new KyouenModel(c)
    config = $.extend
      canvas: $(c)
      model: k
      , config;
    view = new CreateKyouenView(config)
    view.drawKyouen()
    view

  isEnableButton: (config) ->
    return not @hasClass 'disabled'

  disableButton: (config) ->
    @addClass 'disabled'
    this

  enableButton: (config) ->
    @removeClass "disabled"
    this
