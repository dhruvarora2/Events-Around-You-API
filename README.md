# Events-Around-You-API

Instructions To Run :

Register End Point - https://7469ljob9e.execute-api.us-east-1.amazonaws.com/Prod/register

Login End Point - https://7469ljob9e.execute-api.us-east-1.amazonaws.com/Prod/login

Get Events End Point - https://7469ljob9e.execute-api.us-east-1.amazonaws.com/Prod/getevents

Set Preferences End Point - https://7469ljob9e.execute-api.us-east-1.amazonaws.com/Prod/setpreferences

Note For Every End Point - API Key is required.

-----------Register End Point---------------

Sample Request -
```
{
  "emailId": "dhruvarora@nyu.edu",
  "password":"dhruv1234",
  "event": {
    "category": "Film",
    "genre": "Comedy"
  }
}
```

-----------Login End Point---------------

Sample Request - 
```
{
  "emailId": "dhruvarora@nyu.edu",
  "password":"dhruv1234"
}
```

Response : 
```
{
    "isAuthenticated": true,
    "idToken": "JWT Value",
    "accessToken": "Access Token Value"
}
```

-----------Get Events End Point---------------

Sample Request - 
{
}

Headers:

"Authorization" : idToken (From Login Request)

"AccessToken" : Access Token (From Login Request)

-----------Set Preferences End Point---------------

Sample Request - 
```
{
   "category": "Music",
   "genre": "Jazz"
}
```

Headers:

"Authorization" : idToken (From Login Request)

"AccessToken" : Access Token (From Login Request)

*Note For Every End Point - API Key is required.*
