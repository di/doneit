%import doneit
%import datetime
%from datetime import timedelta, datetime
<h1>{{project['name']}}</h1>
<p>Description: {{project['description']}}</p>
<p>Manager: <a href="/users/{{project['admin']['_id']}}">{{project['admin']['name']}}</a></p>
<p>Digest sent at: {{datetime.strptime(project['digest-hour'], '%H').strftime('%l %p EST')}}</p>
<p>Members:
%for user in doneit.get_project_members(project['_id']):
    <a href="/users/{{user['_id']}}">{{user['name']}}</a>
%end
</p>
<p>Post-commit hook URL:<input size="50" value="http://{{doneit.entry_input_service_host}}:{{doneit.entry_input_service_port}}/github?id={{project['_id']}}&key={{project['secret-key']}}"</input></p>
<hr>
<p>
    <a href="?date={{(project['date']-timedelta(days=1)).strftime("%y-%m-%d")}}">< Previous day</a> | 
    <a href="?">Today</a> | 
    <a href="?date={{(project['date']+timedelta(days=1)).strftime("%y-%m-%d")}}">Following day ></a>
</p>
<p>Project status as of <b>{{project['date'].strftime("%B %d, %Y (%A) @ %l %p EST")}}</b></p>
%for type in ['todo', 'doing', 'block', 'done']:
    <b>{{type.title()}}:</b>
    <ul>
    %if project[type].count():
        %for t in project[type]:
            %user = doneit.get_by_id('users', t['user_id'])
            <li>{{t['comment']}} - <a href="/users/{{user['_id']}}">{{user['name']}}</a></li>
        %end
    %else:
        <li><i>None</i></li>
    %end
    </ul>
%end
<p><a href="/projects">< Back to projects</a></p>
%title=project['name']
%rebase layout **locals()
