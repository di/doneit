<h1>Current users:</h1>
<ul>
%for user in users:
<li><a href="/users/{{user['_id']}}">{{user['name']}}</a></li>
%end
</ul>
<p><a href="/">< Back to home</a>
%title='Current Users'
%rebase layout **locals()
