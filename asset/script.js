var auto_at = 0;

function reauto(){
	if(auto_at < 0){
		auto_at = $('#autocomplete > li').length - 1;
	} else if(auto_at > $('#autocomplete > li').length - 1){
		auto_at = 0;
	}
	$($('#autocomplete > li').removeClass('active').get(auto_at)).addClass('active');
}

function autoreset(){
	$('#search').attr('autocomplete', 'on');
	auto_at = 0;
	$('#auto_container').hide();
}

$(document).ready(function(){
	$("img.scaled").load(function(){
		var img = $(this), width = img.width(), height = img.height();
		img.css("max-width", "1000px !important");
		if(width == height) {
			img.width(200).height(200);
		} else if(width > height) {
			img.height(Math.round(height / width * 200)).width(200);
			img.css("margin-top", (200 - img.height()) / 2);
		} else {
			img.width(Math.round(width / height * 200)).height(200);
		}
	});
	$("#search").keydown(function(e){
		if(e.keyCode == 13){
			if($('#auto_container').css("display") == "block"){
				v = '';
				select = $('a', $('#autocomplete > li').get(auto_at) ).attr('data-val');
				words = $(this).val().split(' ');
				for(i = 0;i<=words.length-1;i++){
					if(select.indexOf(words[i]) == 0){
						v = v + select + ' ';
						move = $(this).get(0).selectionEnd + 1;
						for(x = 0;x<= select.length; x++){
							if(words[i].length-1 > x){
								if(words[i].charAt(x) != select.charAt(x)){
									move=move+1;
								}
							} else{ move = move+1; }
						}
					} else{
						v = v + words[i] + ' ';
					}
				}
				$("#search").val(v).get(0).setSelectionRange(move, move);
				return false;
			}
		}
		return true;
	}).keyup(function(e){
		if(e.keyCode == 38){ // Up
			auto_at = auto_at - 1;
			reauto();
		} else if(e.keyCode == 40){ // Down
			auto_at = auto_at + 1;
			reauto();
		} else{
			word = 0;
			words = $(this).val().split(' ');
			for(i=0;i<= $(this).get(0).selectionEnd;i++){
				if($(this).val().charAt(i-1) == ' '){
					word += 1;
				}
			}
			word = words[word];
			if($(this).val().charAt(i) == ' '){ autoreset(); return; }
			if(word.length < 1){ autoreset(); return; }
			// Now look for the phrase
			matches = [];
			for(i=0;i<= keywords.length-1;i++){
				if(keywords[i].indexOf(word) == 0 && keywords[i] != word){
					matches.push(i);
				}
			}
			$('#autocomplete').html('');
			if(matches.length == 0){
				autoreset();
			} else{
				$('#auto_container').show();
				$('#search').attr('autocomplete', 'off');
				for(i=0;i<= matches.length-1;i++){
					li = $('<li>').appendTo('#autocomplete');
					$('<a>').html(kw_ex[matches[i]]).attr('data-val', keywords[matches[i]]).appendTo(li);
				}
			}
			
			reauto();
		}
	});
});
