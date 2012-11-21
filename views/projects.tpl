<h1>Current projects:</h1>
<ul>
%for project in projects:
<li><a href="/projects/{{project['_id']}}">{{project['name']}}</a></li>
%end
</ul>
<p><a href="/">< Back to home</a>
%rebase layout title='Current Projects'
