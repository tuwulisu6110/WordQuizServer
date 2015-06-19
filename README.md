# WordQuizServer
This program is based on Python flask and sqlite. Python flask is used as an interface about sqlite manipulation. And sqlite help us to store accounts and japanese words information. 
wordQuizBackEnd.py is the mainly file of whole program. This file have two parts: one is server interface which is ready to receive HTTP POST request for data manupulation, the other one is a sort of HTTP GET port for web page request as view for user. And there is anthor view made by Android, if you have interest in that here is the link: https://github.com/tuwulisu6110/JPWordQuiz
```
The following lists HTTP POST request(server model) description:
1. path : "/login": 
        required json request tags : ["username","password"]
        return json {"status":string,"serialNum":string,"identifier":string}
    'serialNum' and 'identifier' are needed for other POST request like: addWord, deleteWord ... etc. 
2. path : "/register":
        required json request tags : ["username","password"]
        return json {"status":string}
    This function will generate table for storing words and sources, then record account infomation.
3. path : "/addSoruce":
        required json request tags : ["username","source","serialNum", "identifier"]
        return json {"status":string , "lastId":int}
    'lastId' is the id of source which you added by this request.
4. path : "/listSoruce":
        required json request tags : ["username","serialNum", "identifier"]
        return json {"status":string , "sources":jsonobject}
    'sources' stored a list of pairs that is formatted as {id:sourceName}.
5. path : "/deleteWord":
        required json request tags : ["username","serialNum", "identifier","wordId"]
        return json {"status":string}
    if delete failed, will return error msg.
6. path : "/addWord":
        required json request tags : ["username","serialNum", "identifier"] and ['word','reading','meaning','sourceId','page','sentence']
        return json {"status":string}
    ['word','reading','meaning','sourceId','page','sentence'] is the word information that will be added to database by this request.
7. path : "/searchWordByWordAndReading":
        required json request tags : ["username","serialNum", "identifier"] and ["word"]
        return json {"status":string,"words":jsonArray}
    'words' is a list of jsonObject contains wordInfo. It refers to the function generateJsonWord().
8. path : "/randomWord":
        required json request tags : ["username","serialNum", "identifier"] and ["num"]
        return json {"status":string,"words":jsonArray}
    'words' is a random picked list of jsonObject contains wordInfo. The size of 'words' is determined by 'num'.
9. path : "/recordAnswerResult":
        required json request tags :["username","serialNum", "identifier"] and ["wordId","result"]
        return json {"status":string}
    "result" is an integer for that 1 is correct, 0 is incorrect. Then accumulate to database.
10. path : "/listAllReadingByWord":
        required json request tags :["username","serialNum","identifier"] and ["word"]
        return json {"status":string,"readingList":jsonArray}
        readingList is a reading list from network dictionary goo. 




The following lists HTTP GET request(web page view) description:
1. path: '/loginLobby' return loginLobby.html
    In loginLobby.html, when logging succeed, jump to '/home' for word functions.
2. path: '/home' return home.html
    home.html have 3 sub pages about word functions below.
3. path: '/addNewWordPage' return addNewWordPage.html
4. path: '/searchWordPage' return searchWordPage.html
5. path: '/wordQuizPage' return wordQuizPage.html
All the html file you can find them in /templates.
The js file stored in /static.
```
