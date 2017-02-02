import webapp2
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup Form</title>
    <style>
        .error {
            color: red;
            display: inline;
        }
    </style>
</head>
<body>"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

signup_form ="""
<form action='/welcome' method='post'>
  <table>
    <tr>
      <td>
        <label for=username> Username: </label>
      </td>
      <td>
        <input type="text" name="username" value={username} />
        <p class="error">{username_error}</p>
      </td>
    </tr>
    <tr>
      <td>
        <label for=password> Password: </label>
      </td>
      <td>
        <input type="password" name="password" value=""/>
        <p class="error">{password_error}</p>
      </td>
    </tr>
    <tr>
      <td>
        <label for=verify>Verify Password: </label>
      </td>
      <td>
        <input type="password" name="verify" value="" />
        <p class="error">{verify_error}</p>
      </td>
    </tr>
    <tr>
      <td>
        <label for=email> Email: </label>
      </td>
      <td>
        <input type="email" name="email" value={email} />
        <p class="error">{email_error}</p>
      </td>
    </tr>
  </table>
  <input type='submit' value='Submit'/>"
</form>
"""

# Heleper function to return list of form elements tuples (label, type)
def getFormElements():
    form_types = [("Username","text"),
                ("Password" , "password"),
                ("Verify" , "password"),
                ("Email" , "email")]
    return form_types

# Regular expression helper functions

def valid_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return username and USER_RE.match(username)

def valid_password(password):
    PW_RE = re.compile(r"^.{3,20}$")
    return password and PW_RE.match(password)

def valid_verify(password,verify):
    return verify and password==verify

def valid_email(email):
    EM_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return email or EM_RE.match(email)

# If there is an error, assign error to correct error content
def error_check(form_list):
    """Takes a list of form elements passed through by POST command,
    returns boolean Y if it passes all tests"""
    # If user does not supply a username
    if username =="":
        error_msg = "Please enter a username"
        self.redirect("/?username_error=" + error_msg)

    # If user supplies a bad username
    elif valid_username(username):
        error_msg = "Please enter a valid username"
        self.redirect("/?username_error=" + error_msg)

    # If password is not valid
    elif valid_password(password):
        error_msg = "That password is not valid"
        self.redirect("/?password_error=" + error_msg)

    # If user password does not match
    elif password != verify:
        error_msg = "Passwords do not match"
        self.redirect("/?verify_error=" + error_msg)

    # If email is not valid
    elif valid_email(email):
        error_msg = "Please enter a valid email address"
        self.redirect("/?email_error=" + error_msg)
    return None

# handler classes
class Index(webapp2.RequestHandler):
    """
    Handles requests coming in to '/' (the root of signup site)
    """
    def get(self):
        index_header = "<h1>Signup</h1>"
        content = page_header + index_header + signup_form + page_footer
        self.response.write(content)

    def post(self):
        # look inside the request to figure out what the user typed
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

class WelcomeHandler(webapp2.RequestHandler):
    """
    Handles form post to /welcome;
    Verify all user inputs
    """
    def get(self):
        username = self.request.get("username")
        welcome_message = "<h2>Welcome, " + username + "</h2>"
        content = page_header + welcome_message + page_footer
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', WelcomeHandler)
], debug=True)
