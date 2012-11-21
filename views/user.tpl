<h1>{{user['name']}}</h1>
<p>Full Name: {{user['name']}}</p>
<p>Email: {{user['email']}}</p>

<p><a href="/users">< Back to users</a>
%rebase layout title=user['name']
