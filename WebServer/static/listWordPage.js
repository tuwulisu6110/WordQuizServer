var showedSourceKeyList = [];
var sourceWordTable = {};
function searchWordsBySourceAndUpdateTable(checkedSourceId)
{
    var parameters = prepareSessionData();
    parameters['conditionList']=[{'colume':'sourceId','target':checkedSourceId,'conditionType':'match'}]
    $.ajax(
    {
    type : "POST",
    url : "http://localhost:5003/searchWord",
    data: JSON.stringify(parameters),
    contentType: 'application/json;charset=UTF-8',
    success: function(response) 
             {
                if(response.status=='success')
                {
                    var tableId = 'sourceTable'+checkedSourceId.toString();
                    createWordsTableForm('source'+checkedSourceId.toString(),tableId);
                    var tableBody = generateWordTableHtmlString(response.words);
                    sourceWordTable["source"+checkedSourceId.toString()]=response.words;
                    $('#'+tableId+' tbody').html("");
                    $('#'+tableId+' tbody').append(tableBody);
                    
                }
                else
                    alert(response.status);
             }
    });
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
    searchWordsBySourceAndUpdateTable(checkedSourceId);
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
function refreshAllShowedSourceTab()
{
    for(var i=0;i<showedSourceKeyList.length;i++)
        searchWordsBySourceAndUpdateTable(showedSourceKeyList[i]);
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
    if($('#sourceTabRadioGroup').html()=="")
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
        $("#sourceTabSelectingModal").modal("show");            
    });
    $("#addSourceTabButton").click(function()
    {
        var checkedSourceId = getCheckedSourceId("sourceTabRadioGroup");
        if(checkedSourceId == -2)
            return;
        var checkedSourceName = getCheckedSourceText("sourceTabRadioGroup");
        showedSourceKeyList.push(checkedSourceId);
        refreshShowedSourceIdCookie();
        generateSourceTab(checkedSourceId,checkedSourceName);
    });
    bindDeleteWordButtonDefault('sourceTabContents');
    bindUpdateCancelButtonDefault('sourceTabContents');
    bindUpdateConfirmButton('sourceTabContents',function()
    {
        updateWord(refreshAllShowedSourceTab);
    });
    bindUpdateButton('sourceTabContents',function()
    {
        var wordIndex = parseInt($(this).attr('updatewordindex'));
        var sourceId = parseInt($(this).attr('sourceId'));
        updatedWordCheckedId = sourceWordTable['source'+sourceId.toString()][wordIndex].id;
        updatedSourceCheckedId = sourceId;
        var updateFormHtml = getUpdateFormHtml(sourceWordTable['source'+sourceId.toString()][wordIndex]);
        cachedTableHtml = $(this).parent().parent().html();
        $(this).parent().parent().html(updateFormHtml);
    });
    bindSelectingSoruceButtonDefault('sourceTabContents');
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
