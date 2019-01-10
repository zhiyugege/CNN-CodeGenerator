$(document).ready(function(){

	$(".bg-gray").css({'border':'2px solid white','pointer-events':'none'});
	//获取卷积核信息
	$(".convInfo").change(function(){
		
		var L = $("#convL").val();
		if(L=="") L = "1";
		var W = $("#convW").val();
		if(W=="") W = "3";
		var H = $("#convH").val();
		if(H=="") H = "3";
		var S = $("#convS").val();
		if(S=="") S = "1";
		var P = $("#convP").val();
		if(P=="") P = "1";
		var result = L+'.'+W+'.'+H+'.'+S+'.'+P
		$("#"+GlobalId).find(".info").html(result);

		$("#conv-n").html(L);
		$("#conv-w").html(W);
		$("#conv-h").html(H);
		$("#conv-s").html(S);
		$("#conv-p").html(P);
	})

	//获取池化层信息
	$(".pool-input").change(function(){

		var sign = "";
		var str = "";
		if($("#maxpool").is(":checked")){
		 	sign = "maxpool";
		 	str = "Max";
		 	$("#"+GlobalId).find(".showname").html('MaxPool');
		}
		else{
			sign = "avepool";
			str = "Average";
			$("#"+GlobalId).find(".showname").html('AveragePool');
		} 
		$("#"+GlobalId).find(".info").html(sign);

		$("#pool-info").html(str);

	})

	//获取标准化信息
	$(".norm-input").change(function(){

		var lag = "";
		var str = "";
		if($("#BN").is(":checked")){ 
			lag = "BN";
			str = "Batch"
		}
		else {
			lag = "GN";
			str = "Group";
		}
		$("#"+GlobalId).find(".info").html(lag);
		$("#"+GlobalId).find(".showname").html(lag);
		$("#norm-info").html(str);
	})

	//获取激活函数

	$("#active-select").change(function(){

		var str = $("#active-select").val();
		$("#"+GlobalId).find(".info").html(str);
		$("#act-info").html(str);
		$("#"+GlobalId).find(".showname").html(str);

	})

	//获取
	$("#fully-input").change(function(){

		var str = $("#fully-input").val();
		$("#"+GlobalId).find(".info").html(str);
		$("#fc-info").html(str);
	})

	DrawRect('data','0')


});
