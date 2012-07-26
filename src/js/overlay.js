(function($) {
	$.fn.overlay = function(overlayConfig) {
		var $target = $(this);
		var defaultOption = {
				position: 'fixed',
				bottom: 0,
				left: 0,
				right: 0,
				top: 0,
				backgroundColor: 'rgba(0, 0, 0, 0.5)'
			};
		var option = $.extend(defaultOption, overlayConfig);
		var $overlay = $('#overlay_area');
		if (!$overlay.length) {
			// 存在しない場合は作成
			$overlay = $('<div />').attr({
				id: 'overlay_area'
			});
			$('body').append($overlay);
		}

		$overlay.css(option);
		$overlay.append($target);

		$overlay.click(function(){
			// オーバレイ領域がクリックされた場合は隠す
			$overlay.hide();
			$target.hide();
		});
		$target.click(function(e) {
			// ターゲット領域がクリックされた場合はイベントの伝達を止める
			e.stopPropagation();
		});

		$overlay.show();
		$target.show();
	}
})(jQuery);
