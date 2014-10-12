(function() {
  var $, createPager, scroll;

  createPager = function($pager) {
    var $next, $pager_content, $prev, count, i, index, lastIndex, size, startIndex, _i, _ref;
    size = Number($pager[0].getAttribute("data-size"));
    index = Number($pager[0].getAttribute("data-index"));
    count = 10;
    startIndex = 1;
    lastIndex = Math.floor((size - 1) / count) + 1;
    $prev = $("<div />").css({
      float: "left",
      width: "10%",
      margin: "0 auto"
    }).append("<<").mouseover(function() {
      return scroll($pager_content, -1);
    }).mouseout(function() {
      return clearInterval($pager_content.data("rightScroll"));
    });
    $prev.appendTo($pager);
    $pager_content = $("<div />").attr({
      id: "pager_content"
    }).css({
      float: "left",
      width: "80%",
      overflow: "hidden",
      margin: "0 auto"
    });
    $pager_content.appendTo($pager);
    for (i = _i = 0, _ref = lastIndex - 1; 0 <= _ref ? _i <= _ref : _i >= _ref; i = 0 <= _ref ? ++_i : --_i) {
      $pager_content.append("&nbsp;");
      $pager_content.append($("<a />").attr({
        href: "javascript:loadStage(" + ((startIndex + i - 1) * count) + ")"
      }).text(startIndex + i));
      $pager_content.append("&nbsp;");
    }
    $next = $("<div />").css({
      float: "left",
      width: "10%",
      margin: "0 auto"
    }).append(">>").mouseover(function() {
      return scroll($pager_content, 1);
    }).mouseout(function() {
      return clearInterval($pager_content.data("rightScroll"));
    });
    return $next.appendTo($pager);
  };

  scroll = function($scrollTarget, direction) {
    return $scrollTarget.data("rightScroll", setInterval(function() {
      return $scrollTarget.scrollLeft($scrollTarget.scrollLeft() + direction * 5);
    }, 20));
  };

  $ = jQuery;

  $.fn.extend({
    pager: function(config) {
      var p, _i, _len, _ref, _results;
      _ref = $(this);
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        p = _ref[_i];
        _results.push(createPager($(p)));
      }
      return _results;
    }
  });

  $(function() {
    return $(".pager").pager();
  });

}).call(this);

//# sourceMappingURL=maps/pager.js.map