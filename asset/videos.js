$(document).bind('loading-done', function(){
	$('#bellow-head').html('<div id="vidplayer"></div>');
	$('li.video a').click(function(){
		$('#vidplayer').html($('img', this).attr('data-player'));
		return false;
	});
});
