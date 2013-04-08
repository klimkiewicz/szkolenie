CREATE_USER = "INSERT INTO users(username, password, email) VALUES ('%(username)s', '%(password)s', '%(email)s');"
CREATE_ACTIVE_USER = "INSERT INTO users(username, password, email, is_active) VALUES ('%(username)s', '%(password)s', '%(email)s', 1);"
GET_USER_ID = "SELECT id FROM users WHERE username = '%(username)s';"
SET_ACTIVE = "UPDATE users SET is_active = 1 WHERE id = %(user_id)s;"
ADD_SESSION = "INSERT INTO sessions(sid, user_id) VALUES ('%(sid)s', %(user_id)s);"
ADD_SESSION_NO_USER = "INSERT INTO sessions(sid) VALUES ('%(sid)s');"
GET_USER = "SELECT user_id FROM sessions WHERE sid = '%(sid)s';"
UPDATE_SID = "UPDATE sessions SET user_id = %(user_id)s WHERE sid = '%(sid)s';"
GET_PASSWORD = "SELECT id, password FROM users WHERE username = '%(username)s';"
DELETE_USER = "DELETE FROM users WHERE id = %(user_id)s;"
GET_COMMENTS = "SELECT comment FROM comments;"
CREATE_COMMENT = "INSERT INTO comments(user_id, comment) VALUES (%(user_id)s, '%(comment)s');"


SIGN_UP = """
<!doctype html>
<form method="POST" action="">
<p><label>Your username: <input name="username"></label></p>
<p><label>Your email: <input name="email"></label></p>
<p><label>Your password: <input name="password"></label></p>
<p><input type="submit" value="Sign in"></p>
</form>
"""


ACTIVATE_EMAIL = """
From: noreply@example.com
To: %(email)s

Hi,

Welcome to our service.

Click below link:

%(link)s

to activate.

Bye!
"""


COMMENTS = """
<!doctype html>
<h1>Comments</h1>

<ul>
%(comments)s
</ul>

<h2>Create comment</h2>
<form method="POST" action="">
<p><label>Comment: <input name="comment"></label></p>
<p><input type="submit" value="Post"></p>
</form>
"""


COMMENT = "<li>%(comment)s</li>"
