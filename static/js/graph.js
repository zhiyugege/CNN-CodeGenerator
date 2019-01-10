
var GlobalId = "";
var CurrentLineItem = null;//当前选择的线
var CurrentRectItem = null;//最后选择的节点
var CurrentRectItem1 = null;//当前选则的节点1
var CurrentRectItem2 = null;//当前选则的节点2
var LineList = new Dictionary();//线id，和对象
var RectList = new Dictionary();//所有的节点id和对象
function item() { }
item.prototype = {
    panelId: '', //工作区id
    jd1: '',//节点1id
    jd2: '',//节点2id
    lineName: '默认名称',//线名称
    lineDes: ''//线描述
};
function rectItem() { }
rectItem.prototype = {
    id: '',//节点id，节点标识
    jdName: '默认名称',//节点名称
    jdDes: '',//节点描述
    jdBool: true,//是否可用
    jdColor: ''//节点背景颜色
};
//画线
function DrawLine(x1, y1, x2, y2, id) {
    var htmlLine = '<line class="line" onclick="SelectLine(this)" id="' + id + '" x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '" style="stroke: rgb(255,0,0); stroke-width: 3;cursor: pointer;" marker-end="url(#arrow)"/>';
    try {
        document.getElementById('svgContext').innerHTML += htmlLine;
    }
    catch (e) {
        alert(e);
    }
    return id;
}
//画矩形
var lines = new Array();
var tag = new Array();
function DrawRect(text, id) {

    $('#ControlDiv').append('<div id="' + id + '" div="bj" style="top:'+(parseInt($("#ControlDiv").scrollTop())+20)+'px" class="draggable '+ text+' '+text+'-style'+' " onclick="SelectRect(\'' + id + '\',\''+ text +'\')" ><span class="info" style="display:none"></span><span style="display:none" class="key">' + text + '</span><span class="showname">'+text+'</span></div>');

    $(".draggable").click(function(){

        pannelReset();
        var key = $(this).find(".key").html();
        if(key=='Conv') {
            $(".height1").css("display","none");
            $("#conv-panel").css({"display":"block"});
            // $("#conv-panel").css({"width":"0"});
            // $('#conv-panel').animate({width:"115px"});
        }
        else if(key=='Pool'){
            var poolInfo = $("#pool-info").html();
            $(".height2").css("display","none");
            $("#pool-panel").css({"display":"block"});
            if(poolInfo=='Max') {
                $(this).find(".info").html('maxpool')
                $(this).find(".showname").html('MaxPool')
            }else if(poolInfo=='Average'){
             $(this).find(".info").html('avepool')
             $(this).find(".showname").html('AveragePool')   
            }// $("#pool-panel").css({"width":"0"});
            // $('#pool-panel').animate({width:"115px"});
        }
        else if(key=='Normalization') {
            var normInfo = $("#norm-info").html();
            $(".height3").css("display","none");
            $("#norm-panel").css({"display":"block"});
            if(normInfo=='Batch'){
             $(this).find(".info").html('BN')
             $(this).find(".showname").html('BN')
            }else if(normInfo=='Group'){ 
                $(this).find(".info").html('GN')
                $(this).find(".showname").html('GN')
            }// $("#norm-panel").css({"width":"0"});
            // $('#norm-panel').animate({width:"115px"});
        }
        else if(key=='Active'){
            var acInfo = $("#act-info").html();
            $(".height4").css("display","none");
            $("#act-pool").css({"display":"block"});
            $(this).find(".info").html(acInfo);
            $(this).find(".showname").html(acInfo);
            // $("#act-pool").css({"width":"0"});
            // $('#act-pool').animate({width:"115px"});
        }else if(key=='Fc'){
            $(".height5").css("display","none");
            $("#fc-pool").css({"display":"block"});
            // $("#fc-pool").css({"width":"0"});
            // $('#fc-pool').animate({width:"115px"});
        }   

    })


    $(".draggable").draggable({
        start: function () {
            lines = new Array();
            tag = new Array();
            for (var key in LineList.data) {
                var lineItem = LineList.get(key);
                if (lineItem != null) {
                    if (lineItem.jd1 == $(this).attr('id')) {
                        lines[lines.length] = key;
                        tag[tag.length] = '1';
                    }
                    else if (lineItem.jd2 == $(this).attr('id')) {
                        lines[lines.length] = key;
                        tag[tag.length] = '2';
                    }
                }
            }
        },
        drag: function () {
            if (lines.length > 0) {
                for (var i = 0; i < lines.length; i++) {
                    var line = lines[i];//线id
                    var jdItem = LineList.get(line);
                    GetLinePorint(jdItem.jd1, jdItem.jd2, line);
                }
            }
        },
        stop: function () {
            if ($(this).position().top < 0) {
                $(this).css("top", "0px");
            }
            if ($(this).position().left < 0) {
                $(this).css("left", "0px");
            }
            if ($(this).position().top > $('#ControlDiv').height() - $(this).height()) {
                $(this).css("top", $('#ControlDiv').height() - $(this).height() + "px");
            }
            if ($(this).position().left > $('#ControlDiv').width() - $(this).width()) {
                $(this).css("left", $('#ControlDiv').width() - $(this).width() + "px");
            }
            if (lines.length > 0) {
                for (var i = 0; i < lines.length; i++) {
                    var line = lines[i];//线id
                    var jdItem = LineList.get(line);
                    GetLinePorint(jdItem.jd1, jdItem.jd2, line);
                }
            }
            lines = new Array();
            tag = new Array();
        }
    });
    var item = new rectItem();
    item.id = id;
    RectList.put(item.id, item);
    return id;
}
function pannelReset(){
    $(".detail-info").css("display","none");
    $(".board").css("display","block");
}

//设置属性
function SetAttr(id, Attr, AttrValue) {
    var c = document.getElementById(id);
    c.setAttribute(Attr, AttrValue);
}
//生成guid
function newGuid() {
    var guid = "";
    for (var i = 1; i <= 32; i++) {
        var n = Math.floor(Math.random() * 16.0).toString(16);
        guid += n;
    }
    return guid;
}
$(document).ready(function(){
    $('#ControlDiv').click(function(e){
         if($(e.target).is('.draggable')||$(e.target).is('.line')){
         }else{
             CurrentRectItem = null;
             CurrentRectItem1 = null;
             CurrentRectItem2 = null;
             CurrentLineItem = null;
             ClearAllInput();
         }
    })
})
function functiongraph() {
    $('#ControlDiv').click(function(e){
         if($(e.target).is('.draggable')||$(e.target).is('.line')){
         }else{
             CurrentRectItem = null;
             CurrentRectItem1 = null;
             CurrentRectItem2 = null;
             CurrentLineItem = null;
             ClearAllInput();
         }
    })
}

function ClickRect() {

    CurrentRectItem = null;
    CurrentRectItem1 = null;
    CurrentRectItem2 = null;
    CurrentLineItem = null;
    ClearAllInput();
}
//获取当期选择的节点
function SelectRect(id,name) {

    event = event || window.event;
    event.stopPropagation();
    if (CurrentRectItem1 == null) {
        CurrentRectItem1 = RectList.get(id);
    }
    else if (CurrentRectItem2 == null) {
        CurrentRectItem2 = RectList.get(id);
    }
    else {
        CurrentRectItem1 = RectList.get(id);
        CurrentRectItem2 = null;
    }
    ClearAllInput();
    CurrentRectItem = RectList.get(id);
    //设置样式
    $("[div='bj']").css('color', '#fff');
    if (CurrentRectItem1 != null) {
        $('#' + CurrentRectItem1.id).css('color', 'black');
    }
    if (CurrentRectItem2 != null) {
        $('#' + CurrentRectItem2.id).css('color', 'black');
    }
    if (CurrentRectItem != null) {
        $('#' + CurrentRectItem.id).css('color', 'black');
        SetJD();
    }
    $('#removeJd').show();
    $('#'+name).css({'border':'2px dotted #F39C12','pointer-events':'all'});
    GlobalId = id;

}
//清除所有的文本框内容
function ClearAllInput() {
    $('#jdName').val('');
    $('#jdDes').val('');
    document.getElementById('jdEn').checked = false;
    $('#jdTag').val('');
    $('#removeLine').hide();
    $('#removeJd').hide();

    $('#lineName').val('');
    $('#lineDes').val('');
    $('#lineTag').val('');

 

    $("[div='bj']").css('color', '#fff');

    $(".bg-gray").css({'border':'2px solid white','pointer-events':'none'});
    $("input").val("");


}
//设置节点
function SetJD() {
    $('#jdTag').val(CurrentRectItem.id);
    $('#jdName').val(CurrentRectItem.jdName);
    $('#jdDes').val(CurrentRectItem.jdDes);
    if (CurrentRectItem.jdBool) {
        document.getElementById('jdEn').checked = true;
    }
}
//两个矩形画线
function GetLinePorint(id1, id2, id) {

    var addHeight = parseInt($("#ControlDiv").scrollTop())
        

    var rect1 = $('#' + id1);
    var rect2 = $('#' + id2);

    var x1 = rect1.position().left;
    var y1 = rect1.position().top+addHeight;
    var width1 = rect1.width();
    var height1 = rect1.height();

    var x2 = rect2.position().left;
    var y2 = rect2.position().top+addHeight;
    var width2 = rect2.width();
    var height2 = rect2.height();

    var lineX1, lineY1, lineX2, lineY2;
    //判断上下关系
    if (Math.abs(x1 - x2) > Math.abs(y1 - y2)) {
        //左右关系
        if (x2 > x1) {
            //id2在id1的右面

            //id2的左面是连接点，id1的右面是连接点
            lineX1 = x1 + width1;
            lineX2 = x2 - 10;
        }
        else {
            //id2在id1的左面

            //id2的右面是连接点,id1的左面是连接点
            lineX1 = x1;
            lineX2 = x2 + width2 + 10;
        }
        lineY1 = y1 + height1 / 2;
        lineY2 = y2 + height1 / 2;
    }
    else {
        //上下关系
        if (y1 > y2) {
            //id1在id2的下面

            //id1的上面是连接点，id2的下面是连接点 
            lineY1 = y1;
            lineY2 = y2 + height1 + 10;
        }
        else {
            //id1在id2的上面
            //id1的下面是连接点，id2的上面是连接点
            lineY1 = y1 + height1;
            lineY2 = y2 - 10;
        }
        lineX1 = x1 + width1 / 2;
        lineX2 = x2 + width2 / 2;
    }
    if (id == undefined) {
        //防止重复画线
        for (var LineItemsR in LineList.data) {
            if (LineList.get(LineItemsR) != null) {
                if (LineList.get(LineItemsR).jd1 == id1 && LineList.get(LineItemsR).jd2 == id2) {
                    return;
                }
                if (LineList.get(LineItemsR).jd2 == id1 && LineList.get(LineItemsR).jd1 == id2) {
                    return;
                }
            }
        }

        var panelId = $(".container-fluid").attr('id');
        var lineId = DrawLine(lineX1, lineY1, lineX2, lineY2, newGuid());
        var items = new item();
        items.panelId = panelId;
        items.jd1 = id1;
        items.jd2 = id2;
        LineList.put(lineId, items);
  

    }
    else {
        SetAttr(id, "x1", lineX1);
        SetAttr(id, "x2", lineX2);
        SetAttr(id, "y1", lineY1);
        SetAttr(id, "y2", lineY2);
    }
}
//自定义字典对象
function Dictionary() {
    this.data = new Array();
    this.put = function (key, value) {
        this.data[key] = value;
    };
    this.get = function (key) {
        return this.data[key];
    };
    this.remove = function (key) {
        this.data[key] = null;
    };
    this.isEmpty = function () {
        return this.data.length == 0;
    };
    this.size = function () {
        return this.data.length;
    };
}
//选择线
var SelectLineId;
function SelectLine(obj) {
    var a = $(obj).attr('id');
    event = event || window.event;
    event.stopPropagation();
    SelectLineId = a;
    ClickRect();
    $('#removeLine').css('display','inline-block');
  
    $('#lineTag').val(a);
    CurrentLineItem = LineList.get(a);
    SetLine();
}
//设置线
function SetLine() {
    if (CurrentLineItem != null) {
        $('#lineName').val(CurrentLineItem.lineName);
        $('#lineDes').val(CurrentLineItem.lineDes);
    }
}

//保存接口
function Save() {
    //保存线信息
    for (var lineItem in LineList.data) {
        if (LineList.get(lineItem) != null) {
            var lineId = lineItem;//线id
            var jdi = LineList.get(lineItem).jd1;//节点1
            var jd2 = LineList.get(lineItem).jd2;//节点2
            var x1 = $('#' + lineItem).attr('x1');//节点1 X坐标
            var y1 = $('#' + lineItem).attr('y1');//节点1 Y坐标
            var x2 = $('#' + lineItem).attr('x2');//节点1 X坐标
            var y2 = $('#' + lineItem).attr('y2');//节点1 Y坐标
            var lineName = LineList.get(lineItem).lineName;//线名称
            var lineDes = LineList.get(lineItem).lineDes;//线描述
        }
    }
    //保存节点
    for (var jdItem in RectList.data) {
        if (RectList.get(jdItem) != null) {
            var jdId = jdItem;//节点id
            var jdX = $('#' + jdItem).position().left;//节点X坐标
            var jdY = $('#' + jdItem).position().top;//节点Y坐标
            var jdName = RectList.get(jdItem).jdName;//节点名称
            var jdDes = RectList.get(jdItem).jdDes;//节点说明
            var jdBool = RectList.get(jdItem).jdBool;//节点是否可用
            var jdColor = RectList.get(jdItem).jdColorf;//节点颜色
        }
    }
    //流程名称
    var lcName = $('#lcName').val();
    //流程描述
    var lcDes = $('#lcDes').val();
    //流程标识
    var lcTag = $('#lcTag').val();
    //主流程标识
    var lcz = $('#lczlTag').val();
    //是否可用
    var lcEn = document.getElementById('lcEn').checked;
}

function DrawJd(name) {

    var rectId = DrawRect(name, newGuid());
}
function DrawHX() {
    if (CurrentRectItem1 != null && CurrentRectItem2 != null) {

        GetLinePorint(CurrentRectItem1.id, CurrentRectItem2.id);
    }
}
function DeleteHX() {
    LineList.remove(SelectLineId);  
    $('#' + SelectLineId).remove();
    $('#removeLine').hide();
}
function DeleteJD() {
    if (CurrentRectItem != null) {
        //移除线
        for (var lineItem in LineList.data) {
            if (LineList.get(lineItem) != null) {
                if (LineList.get(lineItem).jd1 == CurrentRectItem.id || LineList.get(lineItem).jd2 == CurrentRectItem.id) {
                    LineList.remove(lineItem);
                    $('#' + lineItem).remove();
                }
            }
        }
        //移除节点
        RectList.remove(CurrentRectItem.id);
        //移除div
        $('#' + CurrentRectItem.id).remove();
        $('#removeJd').hide();
        $(".bg-gray").css({'border':'2px solid white','pointer-events':'none'});
    }
}
function jdNameChange() {
    if (CurrentRectItem != null) {
        CurrentRectItem.jdName = $('#jdName').val();
        $('#' + CurrentRectItem.id).html(CurrentRectItem.jdName);
    }
}
function jdDesChange() {
    if (CurrentRectItem != null) {
        CurrentRectItem.jdDes = $('#jdDes').val();
    }
}
function jdEnChange() {
    if (CurrentRectItem != null) {
        CurrentRectItem.jdBool = document.getElementById('jdEn').checked;
    }
}
function lineNameChange() {
    var lineName = $('#lineName').val();
    if (CurrentLineItem != null) {
        CurrentLineItem.lineName = lineName;
    }
    SetLine();
}
function lineDesChange() {
    var lineDes = $('#lineDes').val();
    if (CurrentLineItem != null) {
        CurrentLineItem.lineDes = lineDes;
    }
    SetLine();
}

function eye()
{
    console.log('LineList:');
    console.log(LineList.data);
    console.log('RectList:');
    console.log(RectList);
}


// eye()