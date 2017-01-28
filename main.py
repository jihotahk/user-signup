import webapp2
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup Form</title>
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
Email: ""

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
            <label>
                Username
                <input type="text" name="username"/>
            </label>
            <label>
                Password
                <input type="password" name="password"/>
            </label>
            <label>
                Verify Password
                <input type="password" name="verify"/>
            </label>
            <label>
                E-mail
                <input type="email" name="email"/>
            </label>
            <input type="submit" value="Add It"/>
        </form>
        """
        content = page_header + signup_form + page_footer
        self.response.write(content)


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
    """
    Handles welcome message page '/welcome'
    """
    def get(self):
        #If all tests successful, get username and send greeting
        username = self.request.get('username')
        welcome_message = "<h2>Welcome, " + username + "</h2>"
        self.response.write(welcome_message)

app = webapp2.WSGIApplication([
    ('/', Index,
    '/welcome', WelcomeHandler
    )
], debug=True)


"""
Regular Expressions
A regular expression is a handy tool for matching text to a pattern. The regular expressions that we're using to validate you input are as follows:


Example code for validating a username is as follows:

  import re

  def valid_username(username):
    return USER_RE.match(username)
More information on using regular expressions in Python can be found here

NOTE: When you go off to make real applications that require form validation, remember that using regex to check an email address is not quite as simple as we make it seem here. See this Stack Overflow question for more on email validation."""
