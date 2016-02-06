
$(document).ready(function() {
	var number = 0;

	$.ajax({
		url:'rows',
		dataType:'JSON',
		success:function(data){

			number = data.rows-5;

		}

	});

	function getArticle(id){

		$.ajax({
			url:'/more',
			dataType:'JSON',
			data:{

				number: id
			},
			success:function(data){
				// string = data.id + ". "+data.title+": "+data.content
				string = "<div class = 'panel panel-default'><div class = 'panel-heading'>"
				 + "<a href=detail/"+ data.id +"><div class = 'text-left' style = 'color:Blue'>" + data.author
				 +"</div><p class = 'text-center' style = 'color:Green'>"
				 +data.title +"</p></a></div><p class = 'panel-body'><p class = 'text-center'>" 
				 +data.content +"</p></p></div></div>"

				$('#additional').append(string);
			}
		});

	}

	$('#load_more_button').click(function(){
		
		if(number>=1){
		getArticle(number);
		number = number -1;
	}
		else{
			$('#load_more_button').hide();
		}

		
		
	});
});