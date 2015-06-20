
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
		if (xmlhttp.readyState==4 && xmlhttp.status==201)
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
			    if(response.status=='success')
			    {
                    if(response.readingList!=undefined)
                    {
                        var readingList = response.readingList;
                        $('#readingSelection option').remove();
                        $('#readingSelection').append('<option value="">select reading</option>');
                        for (var key in response.readingList)
                        {
                            $('#readingSelection').append('<option value="'+readingList[key]+'">'+readingList[key]+'</option>');
                        }    
                        
                        $('#readingSelection').show();
                            
                    }
			    }
			    else
				    alert(response.status);
		     }
    });
}

$(document).ready(function(){
    $('#listReadingButton').click(function()
    {
        listAllReadingByWord($('#wordText').val());
    });
    $('#readingSelection').on('change',function()
    {
        var reading = $('#readingSelection').find(':selected').val();
        $('#readingText').val(reading);
    });
    $('#readingSelection').hide();
});
