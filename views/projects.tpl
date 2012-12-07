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
<label for="digest-hour">Time to send digests:</label>
<select name="digest-hour">
  <option value="24">Midnight</option>
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
%title='Current Projects'
%rebase layout **locals()
