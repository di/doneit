%import doneit
<h1>{{project['name']}}</h1>
<p>Description: {{project['description']}}</p>
<p>Administrator: <a href="/users/{{project['admin']['_id']}}">{{project['admin']['name']}}</a></p>
%for type in ['todo', 'doing', 'block', 'done']:
    <p>{{type.title()}}:</p>
    <ul>
    %for t in project[type]:
        %user = doneit.get_by_id('users', t['user_id'])
        <li>{{t['comment']}} - <a href="/users/{{user['_id']}}">{{user['name']}}</a></li>
    %end
    </ul>
%end

<p><a href="/projects">< Back to projects</a>
%rebase layout title=project['name']
