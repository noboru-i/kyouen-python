(function() {
  var $;

  $ = jQuery;

  $.fn.extend({
    overlay: function(overlayConfig) {
      var $overlay, $target, defaultOption, option;
      $target = $(this);
      defaultOption = {
        position: "fixed",
        bottom: 0,
        left: 0,
        right: 0,
        top: 0,
        backgroundColor: "rgba(0, 0, 0, 0.5)"
      };
      option = $.extend(defaultOption, overlayConfig);
      $overlay = $("#overlay_area");
      if (!$overlay.length) {
        $overlay = $("<div />").attr({
          id: "overlay_area"
        });
        $("body").append($overlay);
      }
      $overlay.css(option);
      $overlay.append($target);
      $overlay.click(function() {
        $overlay.hide();
        return $target.hide();
      });
      $target.click(function(e) {
        return e.stopPropagation();
      });
      $overlay.show();
      return $target.show();
    }
  });

}).call(this);

//# sourceMappingURL=maps/overlay.js.map