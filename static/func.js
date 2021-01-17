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
function checkCookieExpired()
{
	if(getCookie("username")=="")
    {
		document.location.href = "/loginLobby";
        return false;
    }
}
function prepareSessionData()
{ 
	var username = getCookie("username");
	var serialNum = getCookie("serialNum");
	var identifier = getCookie("identifier");
    return {"username":username,"serialNum":serialNum,"identifier":identifier};

}

function changeActiveSection(caller)
{
	document.getElementById("activeSection").innerHTML = document.getElementById(caller).innerHTML;
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
	$('#logoutNav').mouseleave(function(){mouseOut($(this));});
	$('#logoutNav').mouseenter(function(){mouseIn($(this));});
	$('#listWordSectionNav').mouseenter(function(){mouseIn($(this));});
	$('#listWordSectionNav').mouseleave(function(){mouseOut($(this));});
	
    $('#addNewWordSectionNav').click(function()
	{
		if(checkCookieExpired()==false)
            alert("Session expired. Return to login page.");
		$.get('addNewWordPage',function(response,status)
		{
			if(status!='success')
				alert('request for addNewWordPage failed');
			else
			{
				$('#activeSection').html(response);
				//refreshRadioGroup();//in addNewWordPage.js
			}
		});
		
	});
	$('#listAllWordSectionNav').click(function()
	{
		if(checkCookieExpired()==false)
            alert("Session expired. Return to login page.");
		$.get('searchWordPage',function(response,status)
		{
			if(status!='success')
				alert('request for searchWordPage failed');
			else
			{
				$('#activeSection').html(response);
            }
			
		});
		
	});
	$('#readingQuizNav').click(function()
	{
		if(checkCookieExpired()==false)
            alert("Session expired. Return to login page.");
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
		if(checkCookieExpired()==false)
            alert("Session expired. Return to login page.");
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
	$('#logoutNav').click(function()
	{
		if(checkCookieExpired()==false)
            alert("Session expired. Return to login page.");
        var parameters = prepareSessionData();
        $.ajax(
            {
                type:'POST',
                url:'http://localhost:5001/logout',
                data:JSON.stringify(parameters),
                contentType: 'application/json;charset=UTF-8',
                success: function(response)
                        {
                            if(response.status=='success')
                                document.location.href = "/loginLobby";
                            else
                                alert(response.status);
                        }
            }    
            
        );
	});
	$('#listWordSectionNav').click(function()
	{
		if(checkCookieExpired()==false)
            alert("Session expired. Return to login page.");
		$.get('listWordPage',function(response,status)
		{
			if(status!='success')
				alert('request for searchWordPage failed');
			else
			{
				$('#activeSection').html(response);
            }
			
		});
		
	});
	
});
