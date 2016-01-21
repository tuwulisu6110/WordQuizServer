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
			row.insertCell(5).innerHTML = Math.floor(aWord.rate*100).toString() + '%';
			row.insertCell(6).innerHTML = aWord.pick;
			row.insertCell(7).innerHTML = aWord.correct;
			row.insertCell(8).innerHTML = "<input type='button' value = 'delete' onclick = 'deleteWord(" + aWord.id + "," + row.rowIndex + ")'>";
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
			        refreshWordsTable(wordsTable,response);
			    }
			    else
				    alert(response.status);
		     }
    });
}
