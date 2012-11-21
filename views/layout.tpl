<html>
<head>
  <title>{{title or 'No title'}}</title>
</head>
<body>
  <a href="/">Home</a> | 
  %if loggedin:
    <a href="/logout">Logout</a>
  %else:
    <a href="/login">Login</a>
  %end
  %include
</body>
</html>
