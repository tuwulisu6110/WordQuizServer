
function newSource()
{

    var parameters = prepareSessionData();
    var sourceName = prompt("Please enter source name:","");	
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
				    refreshRadioGroup();
			    }
			    else
				    alert(response.status);
		     }
    });
}
function refreshRadioGroup()
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
				    var sources = response.sources;
				    var radioString = "<input type='radio' name='sources' value='-1'>None";
				    for(var key in sources)
					    radioString += "<input type='radio' name='sources' value=" + key + ">" + sources[key];
				    radioGroup.innerHTML = radioString;
			    }
			    else
				    alert(response.status);
		     }
    });
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
	if (window.XMLHttpRequest)
		xmlhttp=new XMLHttpRequest();// code for IE7+, Firefox, Chrome, Opera, Safari
	else
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");// code for IE6, IE5
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4)
		{
			var jsonResponse = JSON.parse(xmlhttp.responseText);
			if(jsonResponse.status=="success")
			{
				document.getElementById("wordText").value = "";
				document.getElementById("readingText").value = "";
				document.getElementById("meaningText").value = "";
				document.getElementById("sentenceText").value = "";
				document.getElementById("pageText").value = "";
			}
            else
            {
                alert(jsonResponse.status);
            }
            $('#readingSelection').hide();
		}
	}
	var parameters = JSON.stringify({"username":username,"serialNum":serialNum,
									"identifier":identifier,"word":word,
									"reading":reading,"meaning":meaning,
									"sourceId":sourceId,"page":page,"sentence":sentence});
	xmlhttp.open("POST","addWord",true);
	xmlhttp.setRequestHeader("Content-type", "application/json; charset=UTF-8");
	xmlhttp.send(parameters);
	
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
                $(selector+' ul').append('<li><a>'+list[i]+'</a></li>');
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
        /*function(response) 
		     {
			    if(response.status=='success')
			    {
                    if(response.readingList!=undefined)
                    {
                        var readingList = response.readingList;
                        $('#readingSelection option').remove();
                        $('#readingSelection').append('<option value="">select reading</option>');
                        for(var i=0;i<readingList.length;i++)
                        {
                            $('#readingSelection').append('<option value="'+readingList[i]+'">'+readingList[i]+'</option>');
                        }
                        
                        $('#readingSelection').show();
                            
                    }
			    }
			    else
				    alert(response.status);
		     }*/
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

$(document).ready(function(){
    $('#listReadingButton').click(function()
    {
        listAllReadingByWord($('#wordText').val());
    });
    $('#listMeaningButton').click(function()
    {
        listAllMeaningByWord($('#wordText').val());
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
    $('#readingSelection').hide();
    $('#meaningSelection').hide();
});
