<h1>Current projects:</h1>
%for project in projects:
<p><a href="/projects/{{project['_id']}}">{{project['name']}}</a></p>
%rebase layout title='Current Projects'
