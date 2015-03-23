function getCookie(cname) 
{
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
    }
    return "";
}
function getCheckedSourceId()
{
	var radioGroup = document.getElementById("sourceRadioGroup");
	var radioButtons = radioGroup.getElementsByTagName("input");
	for(var i=0 ; i< radioButtons.length ; i++)
		if(radioButtons[i].checked)
			return radioButtons[i].value;
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
function deleteWord(wordId,rowId)
{
	var username = getCookie("username");
	var serialNum = getCookie("serialNum");
	var identifier = getCookie("identifier");
	var parameter = {"wordId" : wordId ,"username":username,"serialNum":serialNum,"identifier":identifier};
	$.ajax(
	{
    type : "POST",
    url : "deleteWord",
    data: JSON.stringify(parameter),
    contentType: 'application/json;charset=UTF-8',
    success: function(response) 
		{
			if(response.status=='success')
			{
				var wordsTable = document.getElementById("wordsTable");
				wordsTable.deleteRow(rowId);
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
function searchWord()
{
	var username = getCookie("username");
	var serialNum = getCookie("serialNum");
	var identifier = getCookie("identifier");
	var searchWord = document.getElementById("searchWordText").value;
	if (window.XMLHttpRequest)
		xmlhttp=new XMLHttpRequest();// code for IE7+, Firefox, Chrome, Opera, Safari
	else
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");// code for IE6, IE5
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==201)
		{
			var wordsTable = document.getElementById("wordsTable");
			var jsonResponse = JSON.parse(xmlhttp.responseText);
			refreshWordsTable(wordsTable,jsonResponse);
		}
	}
	var parameters = JSON.stringify({"username":username,"serialNum":serialNum,"identifier":identifier,"word":searchWord});
	xmlhttp.open("POST","searchWordByWordAndReading",true);
	xmlhttp.setRequestHeader("Content-type", "application/json; charset=UTF-8");
	xmlhttp.send(parameters);
	
}
function newSource()
{
	var username = getCookie("username");
	var serialNum = getCookie("serialNum");
	var identifier = getCookie("identifier");
	var sourceName = prompt("Please enter source name:","");
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
				refreshRadioGroup();
			}
		}
	}
	var parameters = JSON.stringify({"username":username,"serialNum":serialNum,"identifier":identifier,"source":sourceName});
	xmlhttp.open("POST","addSource",true);
	xmlhttp.setRequestHeader("Content-type", "application/json; charset=UTF-8");
	xmlhttp.send(parameters);
	
}
function refreshRadioGroup()
{
	var username = getCookie("username");
	var serialNum = getCookie("serialNum");
	var identifier = getCookie("identifier");
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
				var radioGroup = document.getElementById("sourceRadioGroup");
				var sources = jsonResponse.sources;
				var radioString = "<input type='radio' name='sources' value='-1'>None";
				for(var key in sources)
					radioString += "<input type='radio' name='sources' value=" + key + ">" + sources[key];
				radioGroup.innerHTML = radioString;
			}
		}
	}
	var parameters = JSON.stringify({"username":username,"serialNum":serialNum,"identifier":identifier});
	xmlhttp.open("POST","listSource",true);
	xmlhttp.setRequestHeader("Content-type", "application/json; charset=UTF-8");
	xmlhttp.send(parameters);
	
}
function recordResult(wordId,result)
{
	var username = getCookie("username");
	var serialNum = getCookie("serialNum");
	var identifier = getCookie("identifier");
	var parameter = {'wordId':wordId,'result':result,"username":username,"serialNum":serialNum,"identifier":identifier}
	$.ajax(
	{
    type : "POST",
    url : "recordAnswerResult",
    data: JSON.stringify(parameter),
    contentType: 'application/json;charset=UTF-8',
    success: function(response) 
			{
				if(response.status=='success')
				{
					//do nothing
				}
				else
					alert(response.status);
			}
    });
}
var c=0;
var answerId;
function generateQuiz(num)
{
	var username = getCookie("username");
	var serialNum = getCookie("serialNum");
	var identifier = getCookie("identifier");
	var parameter = {'num':num,"username":username,"serialNum":serialNum,"identifier":identifier}
	$.ajax(
	{
    type : "POST",
    url : "randomWord",
    data: JSON.stringify(parameter),
    contentType: 'application/json;charset=UTF-8',
    success: function(response) 
			{
				if(response.status=='success')
				{
					$('#quizType').text('Reading');
					answerId = Math.floor((Math.random() * num));
					//alert(response.words[0].word);
					$('#question').text(response.words[answerId].word);
					$('#answer'+answerId.toString()).text(response.words[answerId].reading);
					$('#answer'+answerId.toString()).click(function()
					{
						$('#result').html('right');
						$('#answer'+answerId.toString()).css('color','red');
						recordResult(response.words[answerId].id,1);//1 for right
						c++;
					});
					//alert(c);
					for(var i=0;i<num;i++)
						if(i!=answerId)
						{
							$('#answer'+i.toString()).text(response.words[i].reading);
							$('#answer'+i.toString()).click(function()
							{
								$('#result').html('wrong');
								$('#answer'+answerId.toString()).css('color','red');
								recordResult(response.words[answerId].id,0);//0 for wrong
							});
						}
					
				}
				else
					alert(response.status);
			}
    });
}

function changeActiveSection(caller)
{
	document.getElementById("activeSection").innerHTML = document.getElementById(caller).innerHTML;
	if(caller == 'addNewWordSection')
		refreshRadioGroup();
	//if(caller == 'ListAllWordSection')
		
}
function mouseIn(text)
{
	//text.style.color = "red";
	//text.style.cursor = "pointer";
	text.css("color","red");
	text.css("cursor","pointer");
}
function mouseOut(text)
{
	//text.style.color = "black";
	//text.style.cursor = "cursor";
	text.css("color","black");
	text.css("cursor","cursor");
}

$(document).ready(function(){
	$('#addNewWordSectionNav').mouseenter(function(){mouseIn($(this));});
	$('#addNewWordSectionNav').mouseleave(function(){mouseOut($(this));});
	$('#listAllWordSectionNav').mouseenter(function(){mouseIn($(this));});
	$('#listAllWordSectionNav').mouseleave(function(){mouseOut($(this));});
	$('#wordQuizNav').mouseleave(function(){mouseOut($(this));});
	$('#wordQuizNav').mouseenter(function(){mouseIn($(this));});
	$('#addNewWordSectionNav').click(function()
	{
		$.get('addNewWordPage',function(response,status)
		{
			if(status!='success')
				alert('request for addNewWordPage failed');
			else
			{
				$('#activeSection').html(response);
				refreshRadioGroup();
			}
		});
		
	});
	$('#listAllWordSectionNav').click(function()
	{
		$.get('searchWordPage',function(response,status)
		{
			if(status!='success')
				alert('request for searchWordPage failed');
			else
			{
				$('#activeSection').html(response);
				searchWord();
			}
			
		});
		
	});
	$('#wordQuizNav').click(function()
	{
		$.get('wordQuizPage',function(response,status)
		{
			if(status!='success')
				alert('request for wordQuizPage failed');
			else
			{
				$('#activeSection').html(response);
				generateQuiz(4);
				$('#next').click(function()
				{
					$('button').css('color','black');
					$('#result').html('');
					generateQuiz(4);
				});
			}
			
		});
	});
	
});
