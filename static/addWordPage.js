
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
