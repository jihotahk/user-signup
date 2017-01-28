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
        }
    </style>
</head>
<body>
    <h1>Signup</h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

# Regular expression helper functions

def valid_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(username)

def valid_password(password):
    PW_RE = re.compile(r"^.{3,20}$")
    return PW_RE.match(password)

def valid_email(email):
    EM_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return EM_RE.match(email)


# handlers
class Index(webapp2.RequestHandler):
    """
    Handles requests coming in to '/' (the root of our site)
    """
    def get(self):
        signup_form =  """
        <form action="/welcome" method="post">
          <table>
            <tr>
              <td>
                <label for="username">Username</label>
              </td>
              <td>
                <input type="text" name="username"/>
              </td>
            </tr>
            <tr>
              <td>
                <label for="password">Password</label>
              </td>
              <td>
                <input type="password" name="password"/>
              </td>
            </tr>
            <tr>
              <td>
                <label for="verify">Verify Password</label>
              </td>
              <td>
                <input type="password" name="verify"/>
              </td>
            </tr>
            <tr>
              <td>
                <label for="email">E-mail</label>
              </td>
              <td>
                <input type="email" name="email"/>
              </td>
            </tr>
            <tr>
              <td>
                <input type="submit" value="Submit"/>
              </td>
            </tr>
          </table>
        </form>
        """
        content = page_header + signup_form + page_footer
        self.response.write(content)

"""
    def post(self):
        # look inside the request to figure out what the user typed
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        #Input verification
        valid_user = valid_username()
        valid_pass = valid_password()
        valid_verif = password == verify

        content = "stuff" # make it look the same
        self.response.write(content)

class WelcomeHandler(webapp2.RequestHandler):

    def get(self):
        #If all tests successful, get username and send greeting
        username = self.request.get('username')
        welcome_message = "<h2>Welcome, " + username + "</h2>"
        self.response.write(welcome_message)
"""


app = webapp2.WSGIApplication([
    ('/', Index
    #'/welcome', WelcomeHandler
    )
], debug=True)
