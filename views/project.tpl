%import doneit
<h1>{{project['name']}}</h1>
<p>Description: {{project['description']}}</p>
<p>Administrator: {{project['admin']['name']}}</p>
<p>Done:</p>
<ul>
%for t in project['done']:
    <li>{{t['comment']}} - {{doneit.get_by_id('users', t['user_id'])['name']}}</li>
%end
</ul>
<p>Todo:</p>
<ul>
%for t in project['todo']:
    <li>{{t['comment']}} - {{doneit.get_by_id('users', t['user_id'])['name']}}</li>
%end
</ul>
<p>Block:</p>
<ul>
%for t in project['block']:
    <li>{{t['comment']}} - {{doneit.get_by_id('users', t['user_id'])['name']}}</li>
%end
</ul>

<p><a href="/projects">< Back to projects</a>
%rebase layout title=project['name']
