var sourceList=[];
var showedSourceKeyList=[];
function refreshSourceList()
{
    var parameters = prepareSessionData();
	$.ajax(
	{
    type : "POST",
    url : "listSource",
    data: JSON.stringify(parameters),
    contentType: 'application/json;charset=UTF-8',
    success: function(response) 
		     {
			    if(response.status=='success')
                {
				    sourceList = response.sources;
                    rebuildSourceTabs();
                }
			    else
				    alert(response.status);
		     }
    });
}
function refreshSourceRadioGroup()
{
    var radioGroup = document.getElementById("sourceRadioGroup");
    var sources = sourceList;
    var radioString;
    if(showedSourceKeyList.indexOf("-1")==-1)
        radioString = "<label><input type='radio' name='sources' value='-1'>None</label><br>";
    else
        radioString = "";
    for(var key in sources)
    {
        if(showedSourceKeyList.indexOf(key)==-1)
        {
            radioString += "<label><input type='radio' name='sources' value=" + key + ">" 
                            + sources[key] + "</label><br>";
        }
    }
	radioGroup.innerHTML = radioString;
    if(radioString=="")
        $('#addSourceTabButton').attr('disabled',true);
    else
        $('#addSourceTabButton').attr('disabled',false);

}
function getCheckedSourceId()
{
	var radioGroup = document.getElementById("sourceRadioGroup");
	var radioButtons = radioGroup.getElementsByTagName("input");
	for(var i=0 ; i< radioButtons.length ; i++)
		if(radioButtons[i].checked)
			return radioButtons[i].value;
    return -2;
}
function getCheckedSourceText()
{
    var checkedId = getCheckedSourceId();
    if(checkedId == -1)
        return "None";
	return sourceList[checkedId];
}
function generateWordTableHtmlString(words)
{
    var html='';
    var wordNum = words.length;
    for(var i=0;i<wordNum;i++)
    {
        html+='<tr rowid = '+words[i].id+'>';
        html+='<td>'+words[i].word+'</td>';
        html+='<td>'+words[i].reading+'</td>';
        html+='<td>'+words[i].meaning+'</td>';
        html+='<td>'+words[i].sourceName+'</td>';
        html+='<td>'+words[i].sentence+'</td>';
        html+='<td>'+Math.floor(words[i].rate*100).toString() + '%'+'</td>';
        html+='<td>'+words[i].pick+'</td>';
        html+='<td>'+words[i].correct+'</td>';
        html+='<td>'+"<input type='button' value = 'delete' wordid = "+words[i].id+" deletebutton/>"+'</td>';
        html+='</tr>'
    }
    return html;
}
function generateSourceTab(checkedSourceId,checkedSourceName)
{
    var newTabHtml = '<li><a data-toggle="tab" href="#source'
                        +checkedSourceId.toString()+'">'
                        +checkedSourceName+
                        '<button type="button" class="close" deletesourceid="'+
                        checkedSourceId.toString()+'">&times;</button></li>';
    $(newTabHtml).insertBefore('#sourceTabs li:last');
    $("#sourceTabContents").append('<div id="source'+checkedSourceId.toString()+'" class="tab-pane fade"></div>');
    var parameters = prepareSessionData();
    parameters['conditionList']=[{'colume':'sourceId','target':checkedSourceId,'conditionType':'match'}]
    $.ajax(
    {
    type : "POST",
    url : "searchWord",
    data: JSON.stringify(parameters),
    contentType: 'application/json;charset=UTF-8',
    success: function(response) 
             {
                if(response.status=='success')
                {
                    var tableId = 'sourceTable'+checkedSourceId.toString();
                    $("#source"+checkedSourceId.toString()).append(
                        '<table id = "'+tableId+'" class="table table-condensed" >');
                    $('#'+tableId).append('<thead><tr></tr></thead>');
                    $('#'+tableId+' thead tr').append('<th>word</th>');
                    $('#'+tableId+' thead tr').append('<th>reading</th>');
                    $('#'+tableId+' thead tr').append('<th>meaning</th>');
                    $('#'+tableId+' thead tr').append('<th>source</th>');
                    $('#'+tableId+' thead tr').append('<th>sentence</th>');
                    $('#'+tableId+' thead tr').append('<th>accuracy</th>');
                    $('#'+tableId+' thead tr').append('<th>pick</th>');
                    $('#'+tableId+' thead tr').append('<th>correct</th>');
                    $('#'+tableId+' thead tr').append('<th>delete</th>');
                    $('#'+tableId).append('<tbody></tbody>');
                    var tableBody = generateWordTableHtmlString(response.words);
                    $('#'+tableId+' tbody').append(tableBody);
                }
                else
                    alert(response.status);
             }
    });
}
function getCheckedSourceIdFromCookie()
{
    var rawCheckSourceIdList = getCookie('showedSourceId_'+getCookie('username'));
    if(rawCheckSourceIdList=="")
        return [];
    else
        return rawCheckSourceIdList.split(',');
}
function rebuildSourceTabs()
{
    for(var i=0;i<showedSourceKeyList.length;i++)
    {
        id = showedSourceKeyList[i];
        if(id=='-1')
            generateSourceTab(id,'None');   
        else
            generateSourceTab(id,sourceList[id]);   
    }
}

function refreshShowedSourceIdCookie()
{
    var ids = '';
    for(var i=0;i<showedSourceKeyList.length;i++)
        ids+=showedSourceKeyList[i]+',';
    setCookie('showedSourceId_'+getCookie('username'),ids.slice(0,ids.length-1),3600);
}

$(document).ready(function(){
    showedSourceKeyList = getCheckedSourceIdFromCookie();
    refreshSourceList();//rebuild source Tabs as well
    $("#addSourceTab").click(function()
    {
        refreshSourceRadioGroup();
        $("#sourceSelectingModal").modal("show");            
    });
    $("#addSourceTabButton").click(function()
    {
        var checkedSourceId = getCheckedSourceId();
        if(checkedSourceId == -2)
            return;
        var checkedSourceName = getCheckedSourceText();
        showedSourceKeyList.push(checkedSourceId);
        refreshShowedSourceIdCookie();
        generateSourceTab(checkedSourceId,checkedSourceName);
    });
    $('#sourceTabContents').on('click',"[deletebutton]",function()
    {
        var deleteWordId = $(this).attr('wordid');
        var parameters = prepareSessionData();
        parameters.wordId=deleteWordId;
        $.ajax(
        {        
            type : 'POST',
            url : 'deleteWord',
            data: JSON.stringify(parameters),
            contentType : 'application/json;charset=UTF-8',
            success: 
            function(response)
            {
                if(response.status=='success')
                {
                    $('[rowid='+deleteWordId+']').remove();
                }        
                else
                    alert(response.status);
            }
        
        });
    });
    $('#sourceTabs').on('click','li [deletesourceid]',function()
    {
        var deleteSourceId = $(this).attr('deletesourceid');
        var indexOfDeleteSourceId = showedSourceKeyList.indexOf(deleteSourceId);
        showedSourceKeyList.splice(indexOfDeleteSourceId,1);
        refreshShowedSourceIdCookie();
        $(this).parent().remove();
        $("#sourceTabContents #source"+deleteSourceId).remove();
    });
});
