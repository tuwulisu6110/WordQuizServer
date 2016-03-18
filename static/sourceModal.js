var sourceList=[];
function refreshSourceList(somethingAfterRefresh)
{
    if(typeof(somethingAfterRefresh)==='undefined')
        somethingAfterRefresh = function(){};
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
				    sourceList = response.sources;
                    somethingAfterRefresh();
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
    return -2;
}

function getCheckedSourceText()
{
    var checkedId = getCheckedSourceId();
    if(checkedId==-1||checkedId==-2)
        return "None";
    else
	    return sourceList[checkedId];
}

function refreshSourceRadioGroup(onPage)
{
    if(typeof(onPage)==='undefined')
        onPage = '';
    var radioGroup = document.getElementById("sourceRadioGroup");
    var sources = sourceList;
    var radioString;
    if(onPage!='listSourcePage')
        radioString = "<label><input type='radio' name='sources' value='-1'>None</label><br>";
    else
    {
        if(showedSourceKeyList.indexOf("-1")==-1)
            radioString = "<label><input type='radio' name='sources' value='-1'>None</label><br>";
        else
            radioString = "";
    }
    for(var key in sources)
    {
        if(onPage!='listSourcePage')
            radioString += "<label><input type='radio' name='sources' value=" + key + ">" 
                            + sources[key] + "</label><br>";
        else
        {
            if(showedSourceKeyList.indexOf(key)==-1)
            {
                radioString += "<label><input type='radio' name='sources' value=" + key + ">" 
                                + sources[key] + "</label><br>";
            }
        }
    }
    radioGroup.innerHTML = radioString;

}
