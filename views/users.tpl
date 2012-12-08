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
<input type="radio" name="daily-digest" value="true" checked>True
<input type="radio" name="daily-digest" value="false">False<br>
<label for="daily-digest">Daily Reminder?:</label>
<input type="radio" name="reminder-email" value="true" checked>True
<input type="radio" name="reminder-email" value="false">False<br>
<label for="project">Project:</label>
<select name="project">
%for project in projects:
    <option value="{{project['_id']}}">{{project['name']}}</option>
%end
</select><br>
<label for="reminder-hour">Time to send daily reminder:</label>
<select name="reminder-hour">
  <option value="0">Midnight</option>
  <option value="1">1 AM</option>
  <option value="2">2 AM</option>
  <option value="3">3 AM</option>
  <option value="4">4 AM</option>
  <option value="5">5 AM</option>
  <option value="6">6 AM</option>
  <option value="7">7 AM</option>
  <option value="8">8 AM</option>
  <option value="9">9 AM</option>
  <option value="10">10 AM</option>
  <option value="11">11 AM</option>
  <option value="12">Noon</option>
  <option value="13">1 PM</option>
  <option value="14">2 PM</option>
  <option value="15">3 PM</option>
  <option value="16">4 PM</option>
  <option value="17">5 PM</option>
  <option value="18">6 PM</option>
  <option value="19">9 PM</option>
  <option value="20">8 PM</option>
  <option value="21">9 PM</option>
  <option value="22">10 PM</option>
  <option value="23">11 PM</option>
</select><br>
<input type="submit" value="Submit">
</form>
%end
<p><a href="/">< Back to home</a>
%title='Current Users'
%rebase layout **locals()
