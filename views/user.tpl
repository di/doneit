%import doneit
%import datetime
%from datetime import datetime
<h1>{{user['name']}}</h1>
<p>Full Name: {{user['name']}}</p>
<p>Email: <a href="mailto:{{user['email']}}">{{user['email']}}</a></p>
%project = doneit.get_by_id('projects', user['project_id'])
<p>Current Project: <a href="/projects/{{user['project_id']}}">{{project['name']}}</a></p>
<p>Receives daily digest: {{user['daily-digest']}}</p>
<p>Receives daily reminder: {{user['reminder-email']}}</p>
<p>Daily reminder time: {{datetime.strptime(user['reminder-hour'], '%H').strftime('%l %p')}}</p>

<p><a href="/users">< Back to users</a>
%title=user['name']
%rebase layout **locals()
