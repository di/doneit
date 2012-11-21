<h1>Login:</h1>
%if failed:
    <i>Login failed</i>
%end
<form method="POST">
<label for="email">Email:</label>
<input type="text" name="email"><br>
<label for="password">Password:</label>
<input type="password" name="password"><br>
<input type="submit" value="Submit">
</form>
<p><a href="/">< Back to home</a>
%title='Login'
%rebase layout **locals()
