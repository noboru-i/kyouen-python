(function() {
  var $, CreateKyouenView, KyouenData, KyouenModel, KyouenView, Line, Point, TumeKyouenView, openKyouen,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  String.prototype.replaceCharAt = function(at, replaceChar) {
    var after, before;
    before = this.substring(0, at);
    after = this.slice(at + 1);
    return before + replaceChar + after;
  };

  KyouenView = (function() {
    function KyouenView(canvas, model) {
      this.canvas = canvas;
      this.model = model;
      this.init();
    }

    KyouenView.prototype.init = function() {};

    KyouenView.prototype.drawKyouen = function() {
      var ctx;
      ctx = this.canvas[0].getContext("2d");
      this.drawBackground(ctx);
      return this.drawStones(ctx);
    };

    KyouenView.prototype.drawClear = function() {
      var $div;
      if (this.model.clear !== "1") {
        return;
      }
      $div = this.canvas.parent().attr("title", "クリア済み");
      return $div.children(".stageno").addClass("clear");
    };

    KyouenView.prototype.getStoneSize = function() {
      var size, stoneSize, width;
      size = this.model.size;
      width = this.canvas.width();
      stoneSize = Math.floor(width / size / 2);
      stoneSize -= width % size;
      return stoneSize;
    };

    KyouenView.prototype.drawBackground = function(ctx) {
      var i, size, stoneSize, width, _i, _results;
      size = this.model.size;
      width = this.canvas.width();
      stoneSize = this.getStoneSize();
      ctx.clearRect(0, 0, width, width);
      ctx.strokeStyle = "rgb(38, 38, 38)";
      ctx.lineWidth = 2;
      ctx.fillStyle = "rgb(0, 218, 0)";
      ctx.fillRect(0, 0, stoneSize * 2 * size, stoneSize * 2 * size);
      ctx.strokeRect(0, 0, stoneSize * 2 * size, stoneSize * 2 * size);
      _results = [];
      for (i = _i = 0; 0 <= size ? _i <= size : _i >= size; i = 0 <= size ? ++_i : --_i) {
        ctx.beginPath();
        ctx.moveTo(stoneSize * 2 * (i + 0.5), 0);
        ctx.lineTo(stoneSize * 2 * (i + 0.5), stoneSize * 2 * size);
        ctx.closePath();
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(0, stoneSize * 2 * (i + 0.5));
        ctx.lineTo(stoneSize * 2 * size, stoneSize * 2 * (i + 0.5));
        ctx.closePath();
        _results.push(ctx.stroke());
      }
      return _results;
    };

    KyouenView.prototype.drawStones = function(ctx) {
      var c, i, index, j, size, stage, stoneSize, _i, _results;
      stage = this.model.stage;
      size = this.model.size;
      stoneSize = this.getStoneSize();
      _results = [];
      for (i = _i = 0; 0 <= size ? _i <= size : _i >= size; i = 0 <= size ? ++_i : --_i) {
        _results.push((function() {
          var _j, _results1;
          _results1 = [];
          for (j = _j = 0; 0 <= size ? _j <= size : _j >= size; j = 0 <= size ? ++_j : --_j) {
            index = i * size + j;
            c = stage.charAt(index);
            switch (c) {
              case "0":
                continue;
              case "1":
                ctx.fillStyle = "rgb(25, 25, 25)";
                break;
              case "2":
                ctx.fillStyle = "rgb(252, 252, 252)";
            }
            ctx.beginPath();
            ctx.arc(stoneSize * 2 * (j + 0.5), stoneSize * 2 * (i + 0.5), stoneSize, 0, Math.PI * 2, false);
            ctx.fill();
            _results1.push(ctx.closePath());
          }
          return _results1;
        })());
      }
      return _results;
    };

    KyouenView.prototype.drawKyouenData = function(ctx, kyouenData) {
      var cx, cy, line, maxScrnWidth, radius, size, startX, startY, stoneSize, stopX, stopY;
      size = this.model.size;
      stoneSize = this.getStoneSize();
      ctx.lineWidth = 5;
      ctx.beginPath();
      ctx.strokeStyle = "rgb(252, 0, 0)";
      if (kyouenData.isLine) {
        line = kyouenData.line;
        startX = 0;
        startY = 0;
        stopX = 0;
        stopY = 0;
        maxScrnWidth = stoneSize * 2 * size;
        if (line.a === 0) {
          startX = 0;
          startY = line.getY(0) * stoneSize * 2 + stoneSize;
          stopX = maxScrnWidth;
          stopY = line.getY(0) * stoneSize * 2 + stoneSize;
        } else if (line.b === 0) {
          startX = line.getX(0) * stoneSize * 2 + stoneSize;
          startY = 0;
          stopX = line.getX(0) * stoneSize * 2 + stoneSize;
          stopY = maxScrnWidth;
        } else {
          if (-1 * line.c / line.b > 0) {
            startX = 0;
            startY = line.getY(-0.5) * stoneSize * 2 + stoneSize;
            stopX = maxScrnWidth;
            stopY = line.getY(size - 0.5) * stoneSize * 2 + stoneSize;
          } else {
            startX = line.getX(-0.5) * stoneSize * 2 + stoneSize;
            startY = 0;
            stopX = line.getX(size - 0.5) * stoneSize * 2 + stoneSize;
            stopY = maxScrnWidth;
          }
        }
        ctx.moveTo(startX, startY);
        ctx.lineTo(stopX, stopY);
        ctx.closePath();
      } else {
        cx = kyouenData.center.x * stoneSize * 2 + stoneSize;
        cy = kyouenData.center.y * stoneSize * 2 + stoneSize;
        radius = kyouenData.radius * stoneSize * 2;
        ctx.arc(cx, cy, radius, 0, Math.PI * 2, false);
      }
      return ctx.stroke();
    };

    KyouenView.prototype.adjust = function(e, kyouen) {
      var canvasX, canvasY, clientRect, pos, size, stoneSize;
      clientRect = e.target.getBoundingClientRect();
      size = kyouen.size;
      stoneSize = this.getStoneSize();
      canvasX = e.clientX - clientRect.left;
      canvasY = e.clientY - clientRect.top;
      pos = {};
      pos.x = Math.ceil(canvasX / stoneSize / 2) - 1;
      pos.y = Math.ceil(canvasY / stoneSize / 2) - 1;
      return pos;
    };

    KyouenView.prototype.showDialog = function(message) {
      var $dialog, $dialogMessage, dialogHeight, dialogWidth;
      $dialog = $("#dialog");
      dialogWidth = $dialog.width();
      dialogHeight = $dialog.height();
      $dialog.css({
        width: dialogWidth + "px",
        height: dialogHeight + "px",
        marginTop: -dialogHeight / 2 + "px",
        marginLeft: -dialogWidth / 2 + "px",
        display: "none"
      });
      $dialogMessage = $("#dialogMessage");
      $dialogMessage.html(message);
      $dialog.click((function(_this) {
        return function(e) {
          if (e.target.id === "dialogMessage") {
            return _this.hideDialog();
          }
        };
      })(this));
      $dialog.hover(function() {
        return $dialog.stop().animate({
          backgroundColor: "#fff",
          color: "#004C9A"
        }, 200);
      }, function() {
        return $dialog.stop().animate({
          backgroundColor: "#eee",
          color: "#333"
        }, 200);
      });
      return $dialog.show(200);
    };

    KyouenView.prototype.hideDialog = function() {
      var _ref;
      return (_ref = $("#dialog")) != null ? _ref.hide() : void 0;
    };

    return KyouenView;

  })();

  openKyouen = function(canvas) {
    var $button, $canvas, $creator, $dialog, $kyouenView, $stageNo, canvasSize, model;
    model = new KyouenModel(canvas);
    canvasSize = Math.floor((Math.min(document.body.clientWidth, document.body.clientHeight, document.documentElement.clientWidth, document.documentElement.clientHeight) - 100) * 0.8);
    canvasSize -= canvasSize % (model.size * 2);
    $kyouenView = $("#kyouenView");
    $kyouenView.overlay();
    $stageNo = $("#stageno0");
    $creator = $("#creator0");
    $canvas = $("#canvas0");
    $button = $("#kyouenButton");
    $dialog = $("#dialog");
    $stageNo.html(model.stageNo);
    $creator.html(model.creator);
    $kyouenView.css({
      width: (canvasSize + 50) + "px",
      height: (canvasSize + 120) + "px"
    });
    $canvas.attr({
      width: canvasSize + "px",
      height: canvasSize + "px",
      "data-stageno": model.stageNo,
      "data-stage": model.stage,
      "data-size": model.size,
      "data-cretor": model.creator,
      "data-clear": model.clear,
      "class": "kyouenView"
    });
    $button.css({
      width: Math.floor(canvasSize * 0.8) + "px"
    });
    $button.disableButton();
    $kyouenView.unbind("click");
    $kyouenView.click(function(e) {
      return e.stopPropagation();
    });
    $kyouenView.show();
    return $canvas[0];
  };

  CreateKyouenView = (function(_super) {
    __extends(CreateKyouenView, _super);

    function CreateKyouenView(config) {
      this.config = config;
      CreateKyouenView.__super__.constructor.call(this, this.config.canvas, this.config.model);
      this.init();
    }

    CreateKyouenView.prototype.init = function() {
      CreateKyouenView.__super__.init.call(this);
      this.canvas.unbind("click");
      return this.canvas.click((function(_this) {
        return function(e) {
          var ctx, index, kyouenData, p, position, positions, _base, _base1, _i, _len, _ref;
          _this.hideDialog();
          position = _this.adjust(e, _this.model);
          _this.model.put(position.x, position.y);
          _this.drawKyouen();
          positions = _this.model.getSelectedStonePositions('1');
          if (positions.length >= 4) {
            kyouenData = _this.model.isKyouenSelected('1');
            if (kyouenData != null) {
              _ref = kyouenData.points;
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                p = _ref[_i];
                index = _this.model.position2Index(p.x, p.y);
                _this.model.stage = _this.model.stage.replaceCharAt(index, '2');
                _this.drawKyouen();
              }
              ctx = _this.canvas[0].getContext("2d");
              _this.drawKyouenData(ctx, kyouenData);
              _this.showDialog("共円！！");
              _this.canvas.unbind("click");
              if (typeof (_base = _this.config).onKyouen === "function") {
                _base.onKyouen(_this.model);
              }
            }
          }
          return typeof (_base1 = _this.config).onChange === "function" ? _base1.onChange(_this.model) : void 0;
        };
      })(this));
    };

    CreateKyouenView.prototype.reset = function() {
      this.hideDialog();
      this.model.resetStage();
      this.init();
      return this.drawKyouen();
    };

    return CreateKyouenView;

  })(KyouenView);

  TumeKyouenView = (function(_super) {
    __extends(TumeKyouenView, _super);

    function TumeKyouenView(canvas, model) {
      this.canvas = canvas;
      this.model = model;
      TumeKyouenView.__super__.constructor.call(this, this.canvas, this.model);
      this.init();
    }

    TumeKyouenView.prototype.init = function() {
      var $button, $dialog;
      TumeKyouenView.__super__.init.call(this);
      this.hideDialog();
      $button = $("#kyouenButton");
      $dialog = $("#dialog");
      this.canvas.unbind("click");
      this.canvas.click((function(_this) {
        return function(e) {
          var position, positions;
          _this.hideDialog();
          position = _this.adjust(e, _this.model);
          _this.model.select(position.x, position.y);
          _this.drawKyouen();
          positions = _this.model.getSelectedStonePositions();
          if (positions.length === 4) {
            return $button.enableButton();
          } else {
            return $button.disableButton();
          }
        };
      })(this));
      $button.unbind("click");
      return $button.click((function(_this) {
        return function(e) {
          var $stageNo, ctx, kyouenData, parentCanvas, parentView;
          if (!$button.isEnableButton()) {
            return;
          }
          kyouenData = _this.model.isKyouenSelected();
          $button.disableButton();
          if (kyouenData != null) {
            _this.canvas.unbind("click");
            ctx = _this.canvas[0].getContext("2d");
            _this.drawKyouenData(ctx, kyouenData);
            $.post("/page/add", {
              stageNo: _this.model.stageNo
            });
            $(_this.model.canvas).attr({
              "data-clear": "1"
            });
            _this.model.clear = "1";
            parentCanvas = $("#canvas" + _this.model.stageNo);
            if (parentCanvas[0] != null) {
              parentView = new KyouenView(parentCanvas, _this.model);
              parentView.drawClear();
            }
            $stageNo = $("#stageno0");
            $stageNo.addClass("clear");
            return _this.showDialog("共円！！");
          } else {
            _this.model.stage = _this.model.stage.replace(/2/g, "1");
            _this.drawKyouen();
            return _this.showDialog("共円ではありません。");
          }
        };
      })(this));
    };

    TumeKyouenView.prototype.drawKyouen = function() {
      var $stageNo;
      TumeKyouenView.__super__.drawKyouen.call(this);
      $stageNo = $("#stageno0");
      if (this.model.clear === "1") {
        return $stageNo.addClass("clear");
      } else {
        return $stageNo.removeClass("clear");
      }
    };

    return TumeKyouenView;

  })(KyouenView);

  KyouenModel = (function() {
    function KyouenModel(canvas) {
      this.stageNo = Number(canvas.getAttribute("data-stageno"));
      this.stage = canvas.getAttribute("data-stage");
      this.size = Number(canvas.getAttribute("data-size"));
      this.creator = canvas.getAttribute("data-creator");
      this.clear = canvas.getAttribute("data-clear");
    }

    KyouenModel.prototype.position2Index = function(x, y) {
      return x + y * this.size;
    };

    KyouenModel.prototype.index2Position = function(index) {
      return new Point(index % this.size, Math.floor(index / this.size));
    };

    KyouenModel.prototype.select = function(x, y) {
      var c, index;
      index = this.position2Index(x, y);
      c = this.stage.charAt(index);
      if (c === "1") {
        return this.stage = this.stage.replaceCharAt(index, "2");
      } else if (c === "2") {
        return this.stage = this.stage.replaceCharAt(index, "1");
      }
    };

    KyouenModel.prototype.put = function(x, y) {
      var c, index;
      index = this.position2Index(x, y);
      c = this.stage.charAt(index);
      if (c === "0") {
        return this.stage = this.stage.replaceCharAt(index, "1");
      }
    };

    KyouenModel.prototype.isKyouenSelected = function(stone) {
      var data, i, j, k, l, p1, p2, p3, p4, selectedStonePositions, _i, _j, _k, _l, _ref, _ref1, _ref2, _ref3, _ref4, _ref5, _ref6;
      if (stone == null) {
        stone = "2";
      }
      selectedStonePositions = this.getSelectedStonePositions(stone);
      if (selectedStonePositions.length < 4) {
        return null;
      }
      for (i = _i = 0, _ref = selectedStonePositions.length - 4; 0 <= _ref ? _i <= _ref : _i >= _ref; i = 0 <= _ref ? ++_i : --_i) {
        p1 = selectedStonePositions[i];
        for (j = _j = _ref1 = i + 1, _ref2 = selectedStonePositions.length - 3; _ref1 <= _ref2 ? _j <= _ref2 : _j >= _ref2; j = _ref1 <= _ref2 ? ++_j : --_j) {
          p2 = selectedStonePositions[j];
          for (k = _k = _ref3 = j + 1, _ref4 = selectedStonePositions.length - 2; _ref3 <= _ref4 ? _k <= _ref4 : _k >= _ref4; k = _ref3 <= _ref4 ? ++_k : --_k) {
            p3 = selectedStonePositions[k];
            for (l = _l = _ref5 = k + 1, _ref6 = selectedStonePositions.length - 1; _ref5 <= _ref6 ? _l <= _ref6 : _l >= _ref6; l = _ref5 <= _ref6 ? ++_l : --_l) {
              p4 = selectedStonePositions[l];
              data = this.isKyouen(p1, p2, p3, p4);
              if (data !== null) {
                return data;
              }
            }
          }
        }
      }
    };

    KyouenModel.prototype.isKyouen = function(p1, p2, p3, p4) {
      var dist1, dist2, intersection123, intersection234, l12, l23, l34;
      l12 = p1.getMidperpendicular(p2);
      l23 = p2.getMidperpendicular(p3);
      intersection123 = this.getIntersection(l12, l23);
      if (intersection123 == null) {
        l34 = p3.getMidperpendicular(p4);
        intersection234 = this.getIntersection(l23, l34);
        if (intersection234 == null) {
          return new KyouenData(p1, p2, p3, p4, true, null, null, new Line(p1, p2));
        }
      } else {
        dist1 = p1.getDistance(intersection123);
        dist2 = p4.getDistance(intersection123);
        if (Math.abs(dist1 - dist2) < 0.0000001) {
          return new KyouenData(p1, p2, p3, p4, false, intersection123, dist1, null);
        }
      }
      return null;
    };

    KyouenModel.prototype.getSelectedStonePositions = function(stone) {
      var c, i, stoneArray, _i, _ref;
      if (stone == null) {
        stone = "2";
      }
      stoneArray = [];
      for (i = _i = 0, _ref = this.size * this.size; 0 <= _ref ? _i <= _ref : _i >= _ref; i = 0 <= _ref ? ++_i : --_i) {
        c = this.stage.charAt(i);
        if (c === stone) {
          stoneArray.push(this.index2Position(i));
        }
      }
      return stoneArray;
    };

    KyouenModel.prototype.getIntersection = function(l1, l2) {
      var det, dx, dy, f1, f2, g1, g2, t1;
      f1 = l1.p2.x - l1.p1.x;
      g1 = l1.p2.y - l1.p1.y;
      f2 = l2.p2.x - l2.p1.x;
      g2 = l2.p2.y - l2.p1.y;
      det = f2 * g1 - f1 * g2;
      if (det === 0) {
        return null;
      }
      dx = l2.p1.x - l1.p1.x;
      dy = l2.p1.y - l1.p1.y;
      t1 = (f2 * dy - g2 * dx) / det;
      return new Point(l1.p1.x + f1 * t1, l1.p1.y + g1 * t1);
    };

    KyouenModel.prototype.hasStone = function(stone) {
      if (stone == null) {
        stone = '1';
      }
      return this.stage.indexOf(stone) !== -1;
    };

    KyouenModel.prototype.resetStage = function() {
      if (this.size === 6) {
        return this.stage = '000000000000000000000000000000000000';
      } else {
        return this.stage = '000000000000000000000000000000000000000000000000000000000000000000000000000000000';
      }
    };

    KyouenModel.prototype.sendStage = function() {
      var callback, param, tmpStage, url;
      url = '/kyouen/regist';
      tmpStage = this.stage.replace(/2/g, '1');
      param = {
        data: [this.size, tmpStage, this.creator].join(',')
      };
      callback = function(data) {
        var reg;
        reg = new RegExp('success stageNo=([0-9]*)');
        if (!data.match(reg)) {
          if (data === 'registered') {
            alert('登録済みです。');
            return;
          }
          alert('送信に失敗しました。');
          return;
        }
        return alert('送信しました。ステージ番号=' + data.replace(reg, '$1'));
      };
      return $.post(url, param, callback);
    };

    KyouenModel.prototype.getStoneCount = function() {
      var count, stage;
      stage = this.stage.replace(/0/g, '');
      count = stage.length;
      return count;
    };

    return KyouenModel;

  })();

  Point = (function() {
    function Point(x, y) {
      this.x = x;
      this.y = y;
    }

    Point.prototype.sum = function(p2) {
      return new Point(this.x + p2.x, this.y + p2.y);
    };

    Point.prototype.difference = function(p2) {
      return new Point(this.x - p2.x, this.y - p2.y);
    };

    Point.prototype.getAbs = function() {
      return Math.sqrt(this.x * this.x + this.y * this.y);
    };

    Point.prototype.getDistance = function(p2) {
      return this.difference(p2).getAbs();
    };

    Point.prototype.getMidpoint = function(p2) {
      return new Point((this.x + p2.x) / 2, (this.y + p2.y) / 2);
    };

    Point.prototype.getMidperpendicular = function(p2) {
      var diff, gradient, midpoint;
      midpoint = this.getMidpoint(p2);
      diff = this.difference(p2);
      gradient = new Point(diff.y, -1 * diff.x);
      return new Line(midpoint, midpoint.sum(gradient));
    };

    return Point;

  })();

  Line = (function() {
    function Line(p1, p2) {
      this.p1 = p1;
      this.p2 = p2;
      this.a = p1.y - p2.y;
      this.b = p2.x - p1.x;
      this.c = p1.x * p2.y - p2.x * p1.y;
    }

    Line.prototype.getY = function(x) {
      return -1 * (this.a * x + this.c) / this.b;
    };

    Line.prototype.getX = function(y) {
      return -1 * (this.b * y + this.c) / this.a;
    };

    return Line;

  })();

  KyouenData = (function() {
    function KyouenData(p1, p2, p3, p4, isLine, center, radius, line) {
      this.points = [p1, p2, p3, p4];
      this.isLine = isLine;
      this.center = center;
      this.radius = radius;
      this.line = line;
    }

    return KyouenData;

  })();

  $ = jQuery;

  $.fn.extend({
    kyouen: function(config) {
      var c, k, view, views, _i, _len, _ref;
      views = [];
      _ref = $(this);
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        c = _ref[_i];
        k = new KyouenModel(c);
        view = new KyouenView($(c), k);
        view.drawKyouen();
        view.drawClear();
        views.push(view);
      }
      return views;
    },
    overlayPlayableKyouen: function(config) {
      return this.click(function() {
        var c, k, view;
        c = openKyouen($("canvas", this)[0]);
        k = new KyouenModel(c);
        view = new TumeKyouenView($(c), k);
        view.drawKyouen();
        view.drawClear();
        return view;
      });
    },
    tumeKyouen: function(config) {
      var c, k, view;
      c = $("canvas", this)[0];
      k = new KyouenModel(c);
      view = new TumeKyouenView($(c), k);
      view.drawKyouen();
      view.drawClear();
      return view;
    },
    createKyouen: function(config) {
      var c, k, view;
      c = this[0];
      k = new KyouenModel(c);
      config = $.extend({
        canvas: $(c),
        model: k
      }, config);
      view = new CreateKyouenView(config);
      view.drawKyouen();
      return view;
    },
    isEnableButton: function(config) {
      return !this.hasClass('disabled');
    },
    disableButton: function(config) {
      this.addClass('disabled');
      return this;
    },
    enableButton: function(config) {
      this.removeClass("disabled");
      return this;
    }
  });

}).call(this);

//# sourceMappingURL=maps/list.js.map