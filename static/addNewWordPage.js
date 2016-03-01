var sourceList;
function newSource()
{

    var parameters = prepareSessionData();
    var sourceName = prompt("Please enter source name:","");	
	if(sourceName==null)
        return;
    parameters.source = sourceName;
	$.ajax(
	{
    type : "POST",
    url : "addSource",
    data: JSON.stringify(parameters),
    contentType: 'application/json;charset=UTF-8',
    success: function(response) 
		     {
			    if(response.status=='success')
			    {
				    refreshSourceRadioGroup();
			    }
			    else
				    alert(response.status);
		     }
    });
}
function deleteSource(deleteMode,sourceId)
{
    var parameters = prepareSessionData();
    parameters.deleteSourceMode = deleteMode;
    parameters.sourceId = sourceId;
	$.ajax(
	{
    type : "POST",
    url : "deleteSource",
    data: JSON.stringify(parameters),
    contentType: 'application/json;charset=UTF-8',
    success: function(response) 
		     {
			    if(response.status=='success')
			    {
                    refreshSourceRadioGroup();
				    alert(response.detail);
			    }
			    else
				    alert(response.status);
		     }
    });

}
function refreshSourceRadioGroup()
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
				    var radioGroup = document.getElementById("sourceRadioGroup");
				    sourceList = response.sources;
                    var sources = sourceList;
				    var radioString = "<label><input type='radio' name='sources' value='-1'>None</label><br>";
				    for(var key in sources)
					    radioString += "<label><input type='radio' name='sources' value=" + key + ">" 
                                        + sources[key] + "</label><br>";
				    radioGroup.innerHTML = radioString;
			    }
			    else
				    alert(response.status);
		     }
    });
}
function getCheckedSourceId()
{
	var radioGroup = document.getElementById("sourceRadioGroup");
	var radioButtons = radioGroup.getElementsByTagName("input");
	for(var i=0 ; i< radioButtons.length ; i++)
		if(radioButtons[i].checked)
			return radioButtons[i].value;
    return -1;
}

function submitWord()
{
	
	var username = getCookie("username");
	var serialNum = getCookie("serialNum");
	var identifier = getCookie("identifier");
	var word = document.getElementById("wordText").value;
	var reading = document.getElementById("readingText").value;
	var meaning = document.getElementById("meaningText").value;
	var sourceId = getCheckedSourceId();
	var sentence = document.getElementById("sentenceText").value;
	var page = document.getElementById("pageText").value;
	if(word=="")
	{
		alert("word can't be empty");
		return;
	}
	var parameters = JSON.stringify({"username":username,"serialNum":serialNum,
									"identifier":identifier,"word":word,
									"reading":reading,"meaning":meaning,
									"sourceId":sourceId,"page":page,"sentence":sentence});
	$.ajax(
	{
    type : "POST",
    url : "addWord",
    data: parameters,
    contentType: 'application/json;charset=UTF-8',
    success: 
        function(response)
        {
            if(response.status=='success')
            {
                document.getElementById("wordText").value = "";
                document.getElementById("readingText").value = "";
                document.getElementById("meaningText").value = "";
                document.getElementById("sentenceText").value = "";
                document.getElementById("pageText").value = "";
            }
            else
                alert(response.status);
            $('#readingSelection').hide();
            $('#meaningSelection').hide();
        }
    });
}

function refreshSelection(response,selectionType)
{    
    if(response.status=='success')
    {
        var selectionName = selectionType + 'Selection';
        var selector = '#' + selectionName;
        var listName = selectionType + 'List';
        var list = response[listName];
        if(list!=undefined)
        {
            $( selector+' ul').remove();
            $( selector ).append('<ul class="dropdown-menu">');
            for(var i=0;i<list.length;i++)
            {
                $(selector+' ul').append('<li><a href=#>'+list[i]+'</a></li>');
            }
            $( selector ).append('</ul>');
            $(selector).show();
                
        }
        else
            alert(selectionType + 'List'+' not exist in response');
    }
    else
        alert(response.status);
}

function listAllReadingByWord(word)
{
    var parameters = prepareSessionData();
    parameters.word=word;
	$.ajax(
	{
    type : "POST",
    url : "listAllReadingByWord",
    data: JSON.stringify(parameters),
    contentType: 'application/json;charset=UTF-8',
    success: function(response)
             {
                refreshSelection(response,'reading');
             }
    });
}


function listAllMeaningByWord(word)
{
    var parameters = prepareSessionData();
    parameters.word=word;
	$.ajax(
	{
    type : "POST",
    url : "listAllMeaningByWord",
    data: JSON.stringify(parameters),
    contentType: 'application/json;charset=UTF-8',
    success: function(response) 
		     {
                 refreshSelection(response,'meaning');
		     }
    });
}

function getCheckedSourceText()
{
    var checkedId = getCheckedSourceId();
    if(checkedId==-1)
        return "None";
    else
	    return sourceList[checkedId];
}
function getCheckedDeleteMode()
{
   return $('#deleteModeRadioGroup input[name=deleteMode]:checked').val(); 
}
$(document).ready(function(){
    refreshSourceRadioGroup();
    $('#listReadingButton').click(function()
    {
        var word = $('#wordText').val();
        if( word == "" || word == null)
        {    
            alert("word cannot be empty!!");
            return;
        }
        listAllReadingByWord(word);
    });
    $('#listMeaningButton').click(function()
    {
        var word = $('#wordText').val();
        if( word == "" || word == null)
        {    
            alert("word cannot be empty!!");
            return;
        }

        listAllMeaningByWord(word);
    });
    $('#readingSelection').on('click','ul li a',function()
    {
        var reading = $(this).text();
        $('#readingText').val(reading);
    });
    $('#meaningSelection').on('click','ul li a',function()
    {
        var meaning = $(this).text();
        $('#meaningText').val(meaning);
    });
    $('#setSourceButton').click(function()
    {
        var selectedSourceText = getCheckedSourceText();
        $("#sourceText").val(selectedSourceText); 
    });
    $('#selectDeleteModeButton').click(function()
    {
        var checkSourceId = getCheckedSourceId();
        if(checkSourceId==-1)
        {
            alert("Should select a valid source.");
        }
        else
        {
            $('#sourceSelectingModal').modal("hide");
            $('#deleteModeSelectingModal').modal("show");
        }   
    });
    $('#deleteSourceButton').click(function()
    {
        var checkedSourceId = getCheckedSourceId();
        var deleteMode = getCheckedDeleteMode();
        deleteSource(deleteMode,checkedSourceId);
    });
});
