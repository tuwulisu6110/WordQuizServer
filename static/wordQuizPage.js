
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
