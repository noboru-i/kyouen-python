(function($) {

	$.fn.kyouenView = function(config) {
		var canvas = $(this);

		for (var i = 0; i < canvas.size(); i++) {
			var c = canvas[i];
			var k = new Kyouen(c);
			drawKyouen(c, k);
			drawClear(c, k);
		}
	};

	$.fn.overlayKyouen = function(config) {
		var targets = this;
		targets.click(function() {
			createPlayableKyouen($('canvas', this)[0]);
		});
	};
	
	$.fn.createPlayableKyouen = function(config) {
		createPlayableKyouen($('canvas', this)[0]);
	}

	$.fn.disableButton = function(config) {
		if (this.button) {
			// jQuery mobileの場合
			this.button('disable');
			this.button('refresh');
		} else {
			// jQueryの場合
			this.attr({
				disabled: "disabled"
			});
		}
		return this;
	}
	
	$.fn.enableButton = function(config) {
		if (this.button) {
			// jQuery mobileの場合
			this.button('enable');
		} else {
			// jQueryの場合
			this.removeAttr("disabled");
		}
		return this;
	}

	// 共円領域の描画
	function drawKyouen(canvas, kyouen) {
		var width = canvas.width;
		var stoneSize = getStoneSize(kyouen.size, width);

		var ctx = canvas.getContext('2d');
		ctx.clearRect(0, 0, width, width);
		
		ctx.strokeStyle ='rgb(38, 38, 38)';
		ctx.lineWidth = 2;
		ctx.fillStyle = 'rgb(0, 218, 0)';
		ctx.fillRect(0, 0, stoneSize * 2 * kyouen.size, stoneSize * 2 * kyouen.size);
		ctx.strokeRect(0, 0, stoneSize * 2 * kyouen.size, stoneSize * 2 * kyouen.size);

		drawBackground(ctx, kyouen.size, stoneSize);
		drawStone(ctx, kyouen.stage, kyouen.size, stoneSize);
	}

	// クリア状態の描画
	function drawClear(canvas, kyouen) {
		if (kyouen.clear !== '1') {
			return;
		}

		$div = $(canvas).parent().attr('title', 'クリア済み');
		$div.children('.stageno').addClass('clear');
	}

	// 石のサイズを返す
	function getStoneSize(size, width) {
		var stoneSize = Math.floor(width / size / 2);
		stoneSize -= width % size;
		
		return stoneSize;
	}
	
	function drawBackground(ctx, size, stoneSize) {
		for (var i = 0; i < size; i++) {
			ctx.beginPath();
			ctx.moveTo(stoneSize * 2 * (i+0.5), 0);
			ctx.lineTo(stoneSize * 2 * (i+0.5), stoneSize * 2 * size);
			ctx.closePath();
			ctx.stroke();
			
			ctx.beginPath();
			ctx.moveTo(0, stoneSize * 2 * (i+0.5));
			ctx.lineTo(stoneSize * 2 * size, stoneSize * 2 * (i+0.5));
			ctx.closePath();
			ctx.stroke();
		}
	}
	
	function drawStone(ctx, stage, size, stoneSize) {

		for (var i = 0; i < size; i++) {
			for (var j = 0; j < size; j++) {
				var index = i * size + j;
				var c = stage.charAt(index);
				if (c === '0') {
					continue;
				}

				if (c === '1') {
					ctx.fillStyle ='rgb(25, 25, 25)';
				} else if (c === '2') {
					ctx.fillStyle ='rgb(252, 252, 252)';
				}
				ctx.beginPath();
				ctx.arc(stoneSize * 2 * (j + 0.5), stoneSize * 2 * (i + 0.5), stoneSize, 0, Math.PI*2, false);
				ctx.fill();
				ctx.closePath();
			}
		}
	}

	function drawKyouenData(ctx, kyouenData, stoneSize, size) {
		ctx.lineWidth = 5;
		ctx.beginPath();

		if (kyouenData.isLine) {
			// 直線の場合
			var line = kyouenData.line;
			var startX = 0;
			var startY = 0;
			var stopX = 0;
			var stopY = 0;
			var maxScrnWidth = stoneSize * 2 * size;
			if (line.a == 0) {
				// x軸と平行な場合
				startX = 0;
				startY = line.getY(0) * stoneSize * 2 + stoneSize;
				stopX = maxScrnWidth;
				stopY = line.getY(0) * stoneSize * 2 + stoneSize;
			} else if (line.b == 0) {
				// y軸と平行な場合
				startX = line.getX(0) * stoneSize * 2 + stoneSize;
				startY = 0;
				stopX = line.getX(0) * stoneSize * 2 + stoneSize;
				stopY = maxScrnWidth;
			} else {
				// 上記以外の場合
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
			// 円の場合
			// 円の場合
			var cx = kyouenData.center.x * stoneSize * 2 + stoneSize;
			var cy = kyouenData.center.y * stoneSize * 2 + stoneSize;
			var radius = kyouenData.radius * stoneSize * 2;

			ctx.arc(cx, cy, radius, 0, Math.PI*2, false);
		}
		ctx.stroke();
	}

	function createPlayableKyouen(canvas) {
		var k = new Kyouen(canvas);

		// 表示領域の高さ・幅のうち、最小のものの8割をcanvasのサイズとする
		var canvasSize = Math.floor(Math.min(document.body.clientWidth,
				document.body.clientHeight,
				document.documentElement.clientWidth,
				document.documentElement.clientHeight) * 0.8);
		canvasSize -= canvasSize % (k.size * 2); // 端数を調整
		
		var $kyouenView = $('#kyouenView');
		if (!$kyouenView.length) {
			// 存在しない場合、作成
			createKyouenView();
			$kyouenView = $('#kyouenView');
		}
		$kyouenView.overlay();
		var $stageNo = $('#stageno0');
		var $creator = $('#creator0');
		var $canvas = $('#canvas0');
		var $button = $('#kyouenButton');
		var $dialog = $('#dialog');
		$stageNo.html(k.stageNo);
		$creator.html(k.creator);
		$kyouenView.css({
				width: (canvasSize + 50) + "px",
				height: (canvasSize + 120) + "px"
			});
		$canvas.attr({
				width: canvasSize + "px",
				height: canvasSize + "px",
				'data-stageno': k.stageNo,
				'data-stage': k.stage,
				'data-size': k.size
			});
		$button.css({
				width: Math.floor(canvasSize * 0.8) + "px"
			});
		$button.disableButton();

		// イベントを設定
		var kyouen = new Kyouen($canvas[0]);
		$kyouenView.unbind('click');
		$kyouenView.click(function(e){
			e.stopPropagation();
		});
		$canvas.unbind('click');
		$canvas.click(function(e) {
				var $dialog = $('#dialog');
				if ($dialog.length) {
					$dialog.remove();
				}
				var position = adjust(e, kyouen);
				kyouen.select(position.x, position.y);
				var positions = kyouen.getSelectedStonePositions();
				if (positions.length == 4) {
					$button.enableButton();
				} else {
					$button.disableButton();
				}
			});
		$button.unbind('click');
		$button.click(function(e) {
				var kyouenData = kyouen.isKyouenSelected();
				$button.disableButton();
				if (kyouenData != null) {
					$canvas.unbind('click');
					var ctx = $canvas[0].getContext('2d');
					var stoneSize = getStoneSize(kyouen.size, $canvas[0].width);
					drawKyouenData(ctx, kyouenData, stoneSize, kyouen.size);
					$.post('/page/add', {'stageNo':kyouen.stageNo});
					$(k.canvas).attr({'data-clear': '1'});
					kyouen.clear = '1';
					drawClear($('#canvas' + kyouen.stageNo)[0], kyouen);
					$stageNo.addClass('clear');
					showDialog('共円！！');
				} else {
					// 未選択状態に戻す
					kyouen.stage = kyouen.stage.replace(/2/g, '1');
					drawKyouen($canvas[0], kyouen);
					showDialog('共円ではありません。');
				}
			});

		$dialog.remove();

		// 共円を描画
		drawKyouen($canvas[0], k);
		if (k.clear === '1') {
			$stageNo.addClass('clear');
		} else {
			$stageNo.removeClass('clear');
		}

		// 共円領域を表示
		$kyouenView.show();
	}

	function showDialog(message) {
		var dialogWidth = $('#kyouenView').width() - 10;
		var dialogHeight = 100;
		var $dialog = $('#dialog');
		var $dialogMessage = $('#dialogMessage');
		if (!$dialog.length) {
			$dialog = $('<div />').attr({
				id : "dialog"
			});
			$dialog.appendTo($('#kyouenView'));
			var $dialogMessage = $('<div />').attr({
				id: "dialogMessage"
			}).css({
				lineHeight: dialogHeight + "px"
			}).html(message);
			$dialogMessage.appendTo($dialog);
		}
		$dialog.css({
				width: dialogWidth + "px",
				height: dialogHeight + "px",
				marginTop: -dialogHeight/2 + "px",
				marginLeft: -dialogWidth/2 + "px",
				display: "none"
			});
		$dialogMessage.html(message);
		$dialog.click(function(e){
			$dialog.remove();
		});
		$dialog.hover(function(){
			$dialog.stop().animate({
				backgroundColor: "#fff",
				color: "#004C9A"
			}, 200);
			$dialog.css({
				textDecoration: "underline"
			});
		}, function() {
			$dialog.stop().animate({
				backgroundColor: "#eee",
				color: "#333"
			}, 200);
			$dialog.css({
				textDecoration: "none"
			});
		});
		$dialog.show(200);
	}
	function removeDialog() {
		var $dialog = $('#dialog');
		if (!$dialog) {
			return;
		}
		$dialog.remove();
	}

	function createKyouenView() {
		var $kyouenView = $('<div />').attr({
				id: "kyouenView"
			});
		$kyouenView.appendTo($('body'));

		var $stageNo = $('<div />').attr({
				id: "stageno0"
			});
		$stageNo.appendTo($kyouenView);

		var $creator = $('<div />').attr({
				id: "creator0"
			});
		$creator.appendTo($kyouenView);

		var $canvas = $('<canvas />').attr({
				id: "canvas0"
			});
		$canvas.appendTo($kyouenView);

		$button = $('<input />').attr({
				id: "kyouenButton",
				type: "button",
				value: "共円！！"
			});
		$button.appendTo($kyouenView);
	}

	function adjust(e, kyouen) {
		var clientRect = e.target.getBoundingClientRect();
		var size = kyouen.size;
		var stoneSize = getStoneSize(size, e.target.width);
		var canvasX = e.clientX - clientRect.left;
		var canvasY = e.clientY - clientRect.top;

		var pos = {};
		pos.x = Math.ceil(canvasX / stoneSize / 2) - 1;
		pos.y = Math.ceil(canvasY / stoneSize / 2) - 1;
		return pos;
	}

	// 文字列の特定の位置の文字を変更
	String.prototype.replaceCharAt = function(at, replaceChar) {
		var before = this.substring(0, at);
		var after = this.slice(at + 1);
		return before + replaceChar + after;
	};
	
	// 共円クラスの定義
	var Kyouen = function(canvas){
		this.obj = this;
		this.canvas = canvas;
		this.stageNo = Number(canvas.getAttribute('data-stageno'));
		this.stage = canvas.getAttribute('data-stage');
		this.size = Number(canvas.getAttribute('data-size'));
		this.creator = canvas.getAttribute('data-creator');
		this.clear = canvas.getAttribute('data-clear');
	};
	Kyouen.prototype = {
		// XY座標をインデックスに変換
		position2Index: function(x, y) {
			return x + y * this.size;
		},

		// インデックスをXY座標に変換
		index2Position: function(index) {
			var pos = new Point(index % this.size, Math.floor(index / this.size));
			return pos;
		},

		// 指定された位置の石を選択
		select: function(x, y) {
			var index = this.position2Index(x, y);
			var c = this.stage.charAt(index);
			if (c === '1') {
				this.stage = this.stage.replaceCharAt(index, '2');
			} else if (c === '2') {
				this.stage = this.stage.replaceCharAt(index, '1');
			}
			drawKyouen(this.canvas, this);
		},
		
		// 共円が選択されている場合、trueを返却
		isKyouenSelected: function() {
			var selectedStonePositions = this.getSelectedStonePositions();
			if (selectedStonePositions.length < 4) {
				return null;
			}
			var p1 = selectedStonePositions[0];
			var p2 = selectedStonePositions[1];
			var p3 = selectedStonePositions[2];
			var p4 = selectedStonePositions[3];
			
			// p1,p2の垂直二等分線を求める
			var l12 = this.getMidperpendicular(p1, p2);
			// p2,p3の垂直二等分線を求める
			var l23 = this.getMidperpendicular(p2, p3);
			
			// 交点を求める
			var intersection123 = this.getIntersection(l12, l23);
			if (intersection123 == null) {
				// p1,p2,p3が直線上に存在する場合
				var l34 = this.getMidperpendicular(p3, p4);
				var intersection234 = this.getIntersection(l23, l34);
				if (intersection234 == null) {
					// p2,p3,p4が直線状に存在する場合
					return new KyouenData(p1, p2, p3, p4, true, null, null, new Line(p1, p2));
				}
			} else {
				var dist1 = this.getDistance(p1, intersection123);
				var dist2 = this.getDistance(p4, intersection123);
				if (Math.abs(dist1 - dist2) < 0.0000001) {
					return new KyouenData(p1, p2, p3, p4, false, intersection123, dist1, null);
				}
			}
			return null;
		},

		// 選択されている石の座標を返却
		getSelectedStonePositions: function() {
			var stoneArray = [];
			for (var i = 0; i < this.size * this.size; i++) {
				var c = this.stage.charAt(i);
				if (c === '2') {
					stoneArray.push(this.index2Position(i));
				}
			}
			return stoneArray;
		},

		// 二点間の距離を求める
		getDistance: function(p1, p2) {
			return p1.difference(p2).getAbs();
		},

		// 交点を求める
		getIntersection: function(l1, l2) {
			var f1 = l1.p2.x - l1.p1.x;
			var g1 = l1.p2.y - l1.p1.y;
			var f2 = l2.p2.x - l2.p1.x;
			var g2 = l2.p2.y - l2.p1.y;

			var det = f2 * g1 - f1 * g2;
			if (det == 0) {
				return null;
			}

			var dx = l2.p1.x - l1.p1.x;
			var dy = l2.p1.y - l1.p1.y;
			var t1 = (f2 * dy - g2 * dx) / det;

			return new Point(l1.p1.x + f1 * t1, l1.p1.y + g1 * t1);
		},

		// 垂直二等分線を求める
		getMidperpendicular: function(p1, p2) {
			var midpoint = this.getMidpoint(p1, p2);
			var diff = p1.difference(p2);
			var gradient = new Point(diff.y, -1 * diff.x);
			
			return new Line(midpoint, midpoint.sum(gradient));
		},
		
		// 中点を求める
		getMidpoint: function(p1, p2) {
			var midpoint = new Point(
					(p1.x + p2.x) / 2,
					(p1.y + p2.y) / 2
				);
			return midpoint;
		}
	};

	// 点情報オブジェクト
	var Point = function(x, y) {
		this.x = x;
		this.y = y;
	};
	Point.prototype = {
		// 和を求める
		sum: function(p2) {
			return new Point(this.x + p2.x, this.y + p2.y);
		},

		// 差を求める
		difference: function(p2) {
			return new Point(this.x - p2.x, this.y - p2.y);
		},

		// 絶対値を求める
		getAbs: function() {
			return Math.sqrt(this.x * this.x + this.y * this.y);
		}
	};

	// 直線情報オブジェクト
	var Line = function(p1, p2) {
		this.p1 = p1;
		this.p2 = p2;
		
		this.a = p1.y - p2.y;
		this.b = p2.x - p1.x;
		this.c = p1.x * p2.y - p2.x * p1.y;
	};
	Line.prototype = {
		getY: function(x) {
			var y = -1 * (this.a * x + this.c) / this.b;
			return y;
		},
		
		getX: function(y) {
			var x = -1 * (this.b * y + this.c) / this.a;
			return x;
		}
	};

	// 共円情報オブジェクト
	var KyouenData = function(p1, p2, p3, p4, isLine, center, radius, line) {
		this.points = [p1, p2, p3, p4];
		this.isLine = isLine;
		this.center = center;
		this.radius = radius;
		this.line = line;
	};
})(jQuery);
