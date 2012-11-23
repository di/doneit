<h1>Add a new Project:</h1>
<form method="POST">
<label for="name">Name:</label>
<input type="text" name="name"><br>
<label for="description">Description:</label>
<input type="text" name="description"><br>
<input type="submit" value="Submit">
</form>
<p><a href="/">< Back to home</a>
%title='Add a new Project'
%rebase layout **locals()
