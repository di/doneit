<h1>Current projects:</h1>
<ul>
%for project in projects:
<li><a href="/projects/{{project['_id']}}">{{project['name']}}</a></li>
%end
</ul>
%if loggedin:
<h1>Add a new Project:</h1>
<form method="POST">
<label for="name">Name:</label>
<input type="text" name="name"><br>
<label for="description">Description:</label>
<input type="text" name="description"><br>
<input type="submit" value="Submit">
</form>
%end
<p><a href="/">< Back to home</a>
%title='Current Projects'
%rebase layout **locals()
