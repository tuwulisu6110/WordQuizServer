function createWordsTableForm(parentId,tableId)
{
    $("#"+parentId).html("");
    $("#"+parentId).append(
        '<table id = "'+tableId+'" class="table table-condensed" >');
    $('#'+tableId).append('<thead><tr></tr></thead>');
    $('#'+tableId+' thead tr').append('<th width="6%">word</th>');
    $('#'+tableId+' thead tr').append('<th width="6%">reading</th>');
    $('#'+tableId+' thead tr').append('<th width="30%">meaning</th>');
    $('#'+tableId+' thead tr').append('<th width="6%">source</th>');
    $('#'+tableId+' thead tr').append('<th width="30%">sentence</th>');
    $('#'+tableId+' thead tr').append('<th width="6%">page</th>');
    $('#'+tableId+' thead tr').append('<th width="6%">update</th>');
    $('#'+tableId+' thead tr').append('<th width="6%">delete</th>');
    $('#'+tableId).append('<tbody></tbody>');

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
        html+='<td>'+words[i].page+'</td>';
        html+='<td>'+"<input type='button' value = 'update' updatewordindex = '"+i+"' sourceId = '"+words[i].sourceId+"'/></td>";
        html+='<td>'+"<input type='button' value = 'delete' wordid = "+words[i].id+" deletebutton/>"+'</td>';
        html+='</tr>'
    }
    return html;
}
function refreshWordsTable(tableId,words)
{
    var tableBody = generateWordTableHtmlString(words);
    $('#'+tableId+' tbody').html('');
    $('#'+tableId+' tbody').append(tableBody);
}
function getUpdateFormHtml(word)
{
    var html = '';
    html+='<td><input type="text" class= "form-control" value = "'+word.word+'" id = "updateWordText"/></td>';
    html+='<td><input type="text" class= "form-control" value = "'+word.reading+'" id = "updateReadingText"/></td>';
    html+='<td><input type="text" class= "form-control" value = "'+word.meaning+'" id = "updateMeaningText"/></td>';
    html+='<td><a id="selectingSourceA">'+word.sourceName+'<a/></td>';
    html+='<td><input type="text" class= "form-control" value = "'+word.sentence+'" id = "updateSentenceText"/></td>';
    html+='<td><input type="text" class= "form-control" value = "'+word.page+'" id = "updatePageText"/></td>';
    html+="<td><input type='button' value = 'comfirm' id='updateComfirm'/></td>";
    html+="<td><input type='button' value = 'cancel' id='updateCancel'/></td>";
    return html;
}
function getUpdateWordInformation()
{
    var aWord={};
    aWord.word=$('#updateWordText').val();
    aWord.reading=$('#updateReadingText').val();
    aWord.meaning=$('#updateMeaningText').val();
    aWord.sourceId=updatedSourceCheckedId;
    aWord.sentence=$('#updateSentenceText').val();
    aWord.page=$('#updatePageText').val();
    aWord.wordId=updatedWordCheckedId;
    return aWord;
}
function updateWord(somethingAfterUpdate)
{
    var parameters = prepareSessionData();
    var word=getUpdateWordInformation();
    parameters.word=word.word;
    parameters.reading=word.reading;
    parameters.meaning=word.meaning;
    parameters.sourceId=word.sourceId;
    parameters.sentence=word.sentence;
    parameters.page=word.page;
    parameters.wordId=word.wordId;
	$.ajax(
	{
    type : "POST",
    url : listWordURL+"updateWord",
    data: JSON.stringify(parameters),
    contentType: 'application/json;charset=UTF-8',
    success: function(response) 
		     {
			    if(response.status=='success')
			    {
                    somethingAfterUpdate();
                                 
			    }
			    else
				    alert(response.status);
		     }
    });
}
function bindUpdateButton(tableDiv,func)
{
    $('#'+tableDiv).on('click',"[updatewordindex]",func);
}
function bindSelectingSoruceButton(tableDiv,func)
{
    $('#'+tableDiv).on('click',"#selectingSourceA",func);
}
function bindUpdateConfirmButton(tableDiv,func)
{
    $('#'+tableDiv).on('click',"#updateComfirm",func);
}
function bindUpdateCancelButton(tableDiv,func)
{
    $('#'+tableDiv).on('click',"#updateCancel",func);
} 
function bindDeleteWordButton(tableDiv,func)
{
    $('#'+tableDiv).on('click',"[deletebutton]",func);
}
function bindUpdateButtonDefault(parentDiv)
{
    bindUpdateButton(parentDiv,function()
    {
        var wordIndex = parseInt($(this).attr('updatewordindex'));
        updatedWordCheckedId = nowWords[wordIndex].id;
        updatedSourceCheckedId = nowWords[wordIndex].sourceId;
        var updateFormHtml = getUpdateFormHtml(nowWords[wordIndex]);
        cachedTableHtml = $(this).parent().parent().html();
        $(this).parent().parent().html(updateFormHtml);
    });
}
function bindSelectingSoruceButtonDefault(parentDiv)
{
    bindSelectingSoruceButton(parentDiv,function()
    {
        refreshSourceList(function()
        {
            refreshSourceList(function(){refreshSourceRadioGroup();});
            $('#sourceSelectingModal').modal('show');
        });
    });
}
function bindUpdateConfirmButtonDefault(parentDiv)
{
    bindUpdateConfirmButton(parentDiv,function()
    {
        //$(this).parent().parent().html(cachedTableHtml);
        updateWord(function()
        {
            searchWord($('#searchWordText').val());
        });
    });
} 
function bindUpdateCancelButtonDefault(parentDiv)
{
    bindUpdateCancelButton(parentDiv,function()
    {
        $(this).parent().parent().html(cachedTableHtml);
    });
}
function bindDeleteWordButtonDefault(parentDiv)
{
    bindDeleteWordButton(parentDiv,function()
    {
        var deleteWordId = $(this).attr('wordid');
        var parameters = prepareSessionData();
        parameters.wordId=deleteWordId;
        $.ajax(
        {
            type : 'POST',
            url : listWordURL+'deleteWord',
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

}
