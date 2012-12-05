<h1>Current users:</h1>
<ul>
%for user in users:
<li><a href="/users/{{user['_id']}}">{{user['name']}}</a></li>
%end
</ul>
%if loggedin:
<h1>Add a new user:</h1>
<form method="POST">
<label for="name">Name:</label>
<input type="text" name="name"><br>
<label for="email">Email:</label>
<input type="text" name="email"><br>
<label for="password">Password:</label>
<input type="password" name="password"><br>
<label for="daily-digest">Daily Digest?:</label>
<input type="radio" name="daily-digest" value="true">True
<input type="radio" name="daily-digest" value="false">False<br>
<label for="project">Project:</label>
<select name="project">
%for project in projects:
    <option value="{{project['_id']}}">{{project['name']}}</option>
%end
</select><br>
<input type="submit" value="Submit">
</form>
%end
<p><a href="/">< Back to home</a>
%title='Current Users'
%rebase layout **locals()
