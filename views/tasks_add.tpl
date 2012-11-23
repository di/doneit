<h1>Add a new task:</h1>
<form method="POST">
<label for="type">Type:</label>
<select name="type">
<option value="todo">TODO</option>
<option value="doing">DOING</option>
<option value="done">DONE</option>
<option value="block">BLOCK</option>
</select><br>
<label for="comment">Comment:</label>
<input type="text" name="comment"><br>
<input type="submit" value="Submit">
</form>
<p><a href="/">< Back to home</a>
%title='Add a new task'
%rebase layout **locals()
