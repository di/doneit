%import doneit
<h1>{{user['name']}}</h1>
<p>Full Name: {{user['name']}}</p>
<p>Email: <a href="mailto:{{user['email']}}">{{user['email']}}</a></p>
%project = doneit.get_by_id('projects', user['project_id'])
<p>Current Project: <a href="/projects/{{user['project_id']}}">{{project['name']}}</a></p>

<p><a href="/users">< Back to users</a>
%rebase layout title=user['name']
