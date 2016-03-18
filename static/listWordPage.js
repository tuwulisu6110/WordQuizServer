var showedSourceKeyList = [];
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
        html+='<td>'+words[i].page+'</td>';
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
                    $('#'+tableId+' thead tr').append('<th>page</th>');
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
        else if(sourceList[id]!=undefined)
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
function controlAddTabButtonOnOff()
{
    if($('#sourceRadioGroup').html()=="")
        $('#addSourceTabButton').attr('disabled',true);
    else
        $('#addSourceTabButton').attr('disabled',false);
}

$(document).ready(function(){
    showedSourceKeyList = getCheckedSourceIdFromCookie();
    refreshSourceList(function()
    {
        duplicateIds = [];
        for(var i = 0;i<showedSourceKeyList.length;i++)
            if(!sourceList[showedSourceKeyList[i]])
                duplicateIds.push(showedSourceKeyList[i]);
        for(var i = 0;i<duplicateIds.length;i++)
            showedSourceKeyList.splice(showedSourceKeyList.indexOf(duplicateIds[i]),1);
        refreshShowedSourceIdCookie();
        rebuildSourceTabs();
    });
    $("#addSourceTab").click(function()
    {
        refreshSourceRadioGroup('listSourcePage');//at sourceModal.js
        controlAddTabButtonOnOff();
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
