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
function checkCookieExpired()
{
	if(getCookie("username")=="")
		document.location.href = "http://220.135.188.70:5000/loginLobby";
}
function prepareSessionData()
{ 
	var username = getCookie("username");
	var serialNum = getCookie("serialNum");
	var identifier = getCookie("identifier");
    return {"username":username,"serialNum":serialNum,"identifier":identifier};

}
function getAllReadingByWord(word)
{
    if(word==undefined||word=="")
    {
        alert('Can\'t reslove empty word');
        return;
    }

}
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
			        var wordsTable = document.getElementById("wordsTable");
			        refreshWordsTable(wordsTable,response);
			    }
			    else
				    alert(response.status);
		     }
    });
}
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
function recordResult(wordId,result)
{
    var parameters = prepareSessionData();
	parameters.result=result;
    parameters.wordId=wordId;
	$.ajax(
	{
    type : "POST",
    url : "recordAnswerResult",
    data: JSON.stringify(parameters),
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
var answerId;

function generateQuiz(num,quizType)
{
    var parameters = prepareSessionData();
	parameters.num=num;
	var title;
	var questionTitleTag, answerTag;
	if(quizType==1)//reading quiz
	{
		title = 'Spell Question';
		questionTitleTag = 'word';
		answerTag = 'reading';
	}
	else if(quizType == 2)//meaning quiz
	{
		title = 'Meaning Question';
		questionTitleTag = 'meaning';
		answerTag = 'word';
	}
	$.ajax(
	{
    type : "POST",
    url : "randomWord",
    data: JSON.stringify(parameters),
    contentType: 'application/json;charset=UTF-8',
    success: function(response) 
			{
				if(response.status=='success')
				{
					$('#quizType').text(title);
					answerId = Math.floor((Math.random() * num));
					//alert(response.words[0].word);
					$('#question').text(response.words[answerId][questionTitleTag]);
					$('#answer'+answerId.toString()).text(response.words[answerId][answerTag]);
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
							$('#answer'+i.toString()).text(response.words[i][answerTag]);
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
	$('#readingQuizNav').mouseleave(function(){mouseOut($(this));});
	$('#readingQuizNav').mouseenter(function(){mouseIn($(this));});
	$('#meaningQuizNav').mouseleave(function(){mouseOut($(this));});
	$('#meaningQuizNav').mouseenter(function(){mouseIn($(this));});
	$('#addNewWordSectionNav').click(function()
	{
		checkCookieExpired();
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
		checkCookieExpired();
		$.get('searchWordPage',function(response,status)
		{
			if(status!='success')
				alert('request for searchWordPage failed');
			else
			{
				$('#activeSection').html(response);
			    fulfillWordTableWithAllWords();
            }
			
		});
		
	});
	$('#readingQuizNav').click(function()
	{
		checkCookieExpired();
		$.get('wordQuizPage',function(response,status)
		{
			if(status!='success')
				alert('request for wordQuizPage failed');
			else
			{
				$('#activeSection').html(response);
				generateQuiz(4,1);//1 for reading quiz
				$('#next').click(function()
				{
					$('button').css('color','black');
					$('#result').html('');
					generateQuiz(4,1);
				});
			}
			
		});
	});
	$('#meaningQuizNav').click(function()
	{
		checkCookieExpired();
		$.get('wordQuizPage',function(response,status)
		{
			if(status!='success')
				alert('request for wordQuizPage failed');
			else
			{
				$('#activeSection').html(response);
				generateQuiz(4,2);//2 for meaning quiz
				$('#next').click(function()
				{
					$('button').css('color','black');
					$('#result').html('');
					generateQuiz(4,2);
				});
			}
			
		});
	});
	
});
