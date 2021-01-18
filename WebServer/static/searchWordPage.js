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
    url : "http://localhost:5003/deleteWord",
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
    url : "http://localhost:5003/searchWordByWordAndReading",
    data: JSON.stringify(parameters),
    contentType: 'application/json;charset=UTF-8',
    success: function(response) 
		     {
			    if(response.status=='success')
			    {
                    nowWords = response.words;
                    refreshWordsTable('wordsTable',response.words);
			    }
			    else
				    alert(response.status);
		     }
    });
}

$(document).ready(function()
{                
    createWordsTableForm('tableDiv','wordsTable');
    fulfillWordTableWithAllWords();//in searchWordPage.js
    bindUpdateButtonDefault('tableDiv');
    bindSelectingSoruceButtonDefault('tableDiv');
    $("#setSourceButton").click(function()
    {
        updatedSourceCheckedId = getCheckedSourceId("sourceRadioGroup");
        if(updatedSourceCheckedId==-2)
            updatedSourceCheckedId = originalSourceId;
        $('#selectingSourceA').html(getCheckedSourceText("sourceRadioGroup"));
    });
    bindUpdateConfirmButtonDefault('tableDiv');
    bindUpdateCancelButtonDefault('tableDiv');
    bindDeleteWordButtonDefault('tableDiv');
});

