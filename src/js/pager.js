(function($) {

	$.fn.pager = function(config) {
		var pager = $(this);

		for (var i = 0; i < pager.size(); i++) {
			var p = pager[i];
			createPager($(p));
		}
	};
	
	function createPager($pager) {
		var size = Number($pager[0].getAttribute('data-size'));
		var index = Number($pager[0].getAttribute('data-index'));
		var count = 10;

		var startIndex = 1
		var lastIndex = Math.floor((size - 1) / count) + 1;

		var $prev = $('<div />').css({
			float: 'left',
			width: '10%',
			margin: '0 auto'
		}).append('<<').mouseover(function() {
			scroll($pager_content, -1);
		}).mouseout(function() {
			clearInterval($pager_content.data('rightScroll'));
		});
		$prev.appendTo($pager);

		var $pager_content = $('<div />').attr({
			id: 'pager_content'
		}).css({
			float: 'left',
			width: '80%',
			overflow: 'hidden',
			margin: '0 auto'
		});
		$pager_content.appendTo($pager);
		for (var i = 0; i < lastIndex; i++) {
			$pager_content.append('&nbsp;')
			$pager_content.append($('<a />').attr({
				href: 'javascript:loadStage(' + ((startIndex + i - 1) * count) + ')'
			}).text(startIndex + i));
			$pager_content.append('&nbsp;')
		}
		
		var $next = $('<div />').css({
			float: 'left',
			width: '10%',
			margin: '0 auto'
		}).append('>>').mouseover(function() {
			scroll($pager_content, 1);
		}).mouseout(function() {
			clearInterval($pager_content.data('rightScroll'));
		});
		$next.appendTo($pager);
	}
	
	function scroll($scrollTarget, direction) {
		$scrollTarget.data('rightScroll', setInterval(function() {
			$scrollTarget.scrollLeft($scrollTarget.scrollLeft() + direction * 5);
		}, 20));
	}
})(jQuery);

$(function() {
	$(".pager").pager();
});