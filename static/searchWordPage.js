var nowWords;
var updatedSourceCheckedId;
var updatedWordCheckedId;
var cachedTableHtml;
var originalSourceId;
function deleteWord(wordId,rowId)
{
    var parameters = prepareSessionData();
    parameters.wordId=wordId;
	$.ajax(
	{
    type : "POST",
    url : "deleteWord",
    data: JSON.stringify(parameters),
    contentType: 'application/json;charset=UTF-8',
    success: function(response) 
		{
			if(response.status=='success')
			{
                searchWord($('#searchWordText').val());                    
			}
			else
				alert(response.status);
		}
    });
}

function refreshWordsTable(wordsTable,jsonResponse)
{
	if(jsonResponse.status=="success")
	{
		var rowLength = wordsTable.rows.length;
		for(var i =0;i<rowLength;i++)
			wordsTable.deleteRow(0);
		for(var i = 0; i<jsonResponse.words.length ; i++)
		{
			var row = wordsTable.insertRow(-1);
			var aWord = jsonResponse.words[i];
			row.insertCell(0).innerHTML = aWord.word;
			row.insertCell(1).innerHTML = aWord.reading;
			row.insertCell(2).innerHTML = aWord.meaning;
			row.insertCell(3).innerHTML = aWord.sourceName;
			row.insertCell(4).innerHTML = aWord.sentence;
			row.insertCell(5).innerHTML = aWord.page;
			row.insertCell(6).innerHTML = "<input type='button' value = 'update' updatewordindex = '"+i+"'/>";
            row.insertCell(7).innerHTML = "<input type='button' value = 'delete' onclick = 'deleteWord(" + aWord.id + "," + row.rowIndex + ")'>";
		}
	}
}

function fulfillWordTableWithAllWords()
{
    searchWord("");
}

function searchWord(targetWord)
{
    var parameters = prepareSessionData();
	parameters.word=targetWord;
	$.ajax(
	{
    type : "POST",
    url : "searchWordByWordAndReading",
    data: JSON.stringify(parameters),
    contentType: 'application/json;charset=UTF-8',
    success: function(response) 
		     {
			    if(response.status=='success')
			    {
			        var wordsTable = document.getElementById("wordsTable").getElementsByTagName('tbody')[0];
			        nowWords = response.words;
                    refreshWordsTable(wordsTable,response);
			    }
			    else
				    alert(response.status);
		     }
    });
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
function updateWord()
{
    var parameters = prepareSessionData();
    parameters.word=$('#updateWordText').val();
    parameters.reading=$('#updateReadingText').val();
    parameters.meaning=$('#updateMeaningText').val();
    parameters.sourceId=updatedSourceCheckedId;
    parameters.sentence=$('#updateSentenceText').val();
    parameters.page=$('#updatePageText').val();
    parameters.wordId=updatedWordCheckedId;
	$.ajax(
	{
    type : "POST",
    url : "updateWord",
    data: JSON.stringify(parameters),
    contentType: 'application/json;charset=UTF-8',
    success: function(response) 
		     {
			    if(response.status=='success')
			    {
                    searchWord($('#searchWordText').val());                    
			    }
			    else
				    alert(response.status);
		     }
    });
}
$(document).ready(function()
{
    $('#wordsTable').on('click',"[updatewordindex]",function()
    {
        var wordIndex = parseInt($(this).attr('updatewordindex'));
        updatedWordCheckedId = nowWords[wordIndex].id;
        updatedSourceCheckedId = nowWords[wordIndex].sourceId;
        var updateFormHtml = getUpdateFormHtml(nowWords[wordIndex]);
        cachedTableHtml = $(this).parent().parent().html();
        $(this).parent().parent().html(updateFormHtml);
        xxx();        
    });
    $('#wordsTable').on('click',"#selectingSourceA",function()
    {
        refreshSourceList(function()
        {
            refreshSourceList(function(){refreshSourceRadioGroup();});
            $('#sourceSelectingModal').modal('show');
        });
    });
    $("#setSourceButton").click(function()
    {
        updatedSourceCheckedId = getCheckedSourceId();
        if(updatedSourceCheckedId==-2)
            updatedSourceCheckedId = originalSourceId;
        $('#selectingSourceA').html(getCheckedSourceText());
    });
    $('#wordsTable').on('click',"#updateComfirm",function()
    {
        fulfillWordTableWithAllWords();
        updateWord();
    });
    $('#wordsTable').on('click',"#updateCancel",function()
    {
        $(this).parent().parent().html(cachedTableHtml);
    });
});

