<h1>{{project['name']}}</h1>
<p>Description: {{project['description']}}</p>
<p>Administrator: {{project['admin']['name']}}</p>
<p><a href="/projects">< Back to projects</a>
%rebase layout title=project['name']
