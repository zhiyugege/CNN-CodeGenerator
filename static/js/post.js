function getLineInfo() 
{

	var lineInfoList = LineList.data;	
	var currentList = [];
	var nodeList = [];
	var lineInfo = [];

	for(var lineItem in LineList.data) {
		if(LineList.get(lineItem) != null) {
			var panelId = LineList.get(lineItem).panelId;
			if(panelId==GlobalPanelId) {
				var jd1 = LineList.get(lineItem).jd1;
				var jd2 = LineList.get(lineItem).jd2;
				if(nodeList.indexOf(jd1)==-1) nodeList.push(jd1);
				if(nodeList.indexOf(jd2)==-1) nodeList.push(jd2);
				currentList.push(LineList.get(lineItem));
				lineInfo.push(jd1+'-'+jd2);
			}
		}
	}
	var info = {'currentList':currentList, 'nodeList':nodeList, 'lineInfo':lineInfo};
	return info;
	// console.log(currentList);

}
function getNodeInfo(nodeList) {
	
	var NodeInfo={};
	for(var i=0;i<nodeList.length;i++)
	{
		var id = nodeList[i];
		var key = $("#"+id).find('.key').html();
		var info = $("#"+id).find('.info').html();
		if(key=='data') {
			if(info=='') info='3'	
			NodeInfo[id] = info;
		}
		else if(key=='Conv') {
			if(info=='') info='1.3.3.1.1';
			NodeInfo[id] = '1-'+info;
		}
		else if(key=='Pool') {
			if(info=='') info='maxpool.3.1';
			NodeInfo[id] = '2-'+info;
		}
		else if(key=='Normalization') {
			if(info=='') info='BN';
			NodeInfo[id] = '3-'+info;
		}
		else if(key=='Active') {
			if(info=='') info='sigmoid';
			NodeInfo[id] = '4-'+info;
		}
		else if(key=='Fc') {
			if(info=='') info='2';
			NodeInfo[id] = '5-'+info;
		}
		else if(key=='Concat') {
			if(info=='') info='0';
			NodeInfo[id] = '6-'+info;
		}
	}	
	return NodeInfo;
}


function generate()
{
	// console.log(GlobalPanelId);
	// console.log('LineList:');
	// console.log(LineList);
 //    console.log(LineList.data);
 //    console.log('RectList:');
 //    console.log(RectList);
    var info = getLineInfo();
    var currentLineInfoList = info.currentList;
    var currentNodeList = info.nodeList;
    var LineInfo = info.lineInfo;
    var NodeInfo = getNodeInfo(currentNodeList);
    console.log(NodeInfo,LineInfo);
    post(NodeInfo,LineInfo);
}
function post(NodeInfo,LineInfo) {

	var  url = '/apps/GenerateApi/';
	var data = {NodeInfo:JSON.stringify(NodeInfo),LineInfo:LineInfo};
	$.ajax({
		url: url,
		data: data,
		type: 'POST',
		dataType: 'json',
		traditional:true,
		headers: {
			'X-CSRFToken':csrf_token
		},
		success: function(res, status) {

		},
		error: function(err) {
			console.log(err);
		}

	})
}