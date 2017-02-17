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

index_h1 = "<h1>Signup</h1>"

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

signup_form ="""
<form action='/'' method ='post'>
  <table>
    <tr>
      <td>
        <label for=username> Username: </label>
      </td>
      <td>
        <input type="text" name="username" value="%(username)s" />
        <p class="error">%(username_error)s</p>
      </td>
    </tr>
    <tr>
      <td>
        <label for=password> Password: </label>
      </td>
      <td>
        <input type="password" name="password" value=""/>
        <p class="error">%(password_error)s</p>
      </td>
    </tr>
    <tr>
      <td>
        <label for=verify>Verify Password: </label>
      </td>
      <td>
        <input type="password" name="verify" value="" />
        <p class="error">%(verify_error)s</p>
      </td>
    </tr>
    <tr>
      <td>
        <label for="email"> Email (Optional): </label>
      </td>
      <td>
        <input type="text" name="email" value="%(email)s" />
        <p class="error">%(email_error)s</p>
      </td>
    </tr>
  </table>
  <input type='submit' value='Submit'/>
</form>
"""

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
    return not email or EM_RE.match(email)

# handler classes
class Index(webapp2.RequestHandler):
    """
    Handles requests coming in to '/' (the root of signup site)
    """
    def write_form(self, username="", email="", username_error="", password_error="", verify_error="", email_error=""):
        content = page_header + index_h1+ signup_form + page_footer
        self.response.out.write(content % { "username": username,
                                            "email": email,
                                            "username_error": username_error,
                                            "password_error": password_error,
                                            "verify_error": verify_error,
                                            "email_error": email_error})

    def get(self):
        #need to set all the string subs to empty string
        self.write_form()

    def post(self):
        #initialize parameter dictionary
        params = {}

        # look inside the request to figure out what the user typed
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        #store username/email, and error messages in a dictionary
        if username:
            params["username"] = username
        if email:
            params["email"] = email

        #Start checking for errors, set form_error to true and set error message
        form_error = False

        # If username not valid
        if not valid_username(username):
            params['username_error'] = "Please enter a valid username"
            form_error = True

        # If password is not valid
        if not valid_password(password):
            params['password_error'] = "That password is not valid"
            form_error = True

        # If user password does not match
        if password != verify:
            params['verify_error'] = "Passwords do not match"
            form_error = True

        # If email is not valid
        if not valid_email(email):
            params['email_error'] = "Please enter a valid email address"
            form_error = True

        #If there is error, rerender with error messages:
        if form_error:
            self.write_form(**params)
        else:
            self.redirect('/welcome?username=' + username)

class WelcomeHandler(webapp2.RequestHandler):
    """
    Handles form post to /welcome;
    """
    def get(self):
        username = self.request.get("username")
        if valid_username:
            welcome_message = "<h2>Welcome, " + username + "!</h2>"
            content = page_header + welcome_message + page_footer
            self.response.write(content)
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', WelcomeHandler)
], debug=True)
