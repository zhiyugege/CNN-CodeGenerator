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
		console.log(GlobalId);
	})

	//获取池化层信息
	$(".pool-input").change(function(){

		var sign = "";
		if($("#maxpool").is(":checked")) sign = "maxpool";
		else sign = "avepool";
		$("#"+GlobalId).find(".info").html(sign);

	})

	//获取标准化信息
	$(".norm-input").change(function(){

		var lag = ""
		if($("#BN").is(":checked")) lag = "BN";
		else lag = "GN";
		$("#"+GlobalId).find(".info").html(lag);

	})

	//获取激活函数

	$("#active-select").change(function(){

		$("#"+GlobalId).find(".info").html($("#active-select").val());

	})

	//获取
	$("#fully-input").change(function(){

		$("#"+GlobalId).find(".info").html($("#fully-input").val());
	})















});






