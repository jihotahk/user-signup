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
<body>"""


# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
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

        # Header elements
        index_header = "<h1>Signup</h1>"

        #store error message if it exists
        user_error = self.request.get("username_error")
        if user_error:
            user_error_span = "<span class='error'>" + user_error + "</span>"
        else:
            user_error_span = ""

        password_error = self.request.get("password_error")
        if password_error:
            password_error_span = "<span class='error'>" + password_error + "</span>"
        else:
            user_error_span = ""

        verify_error = self.request.get("verify_error")
        email_error = self.request.get("email_error")

        if user_error:
            user_error_span = "<span class='error'>" + error + "</span>"
        else:
            user_error_span = ""

        # Build each form element using for loop
        form_table_elements = ""

        for form_label, form_type in getFormElements():
            form_table_elements += """
                    <tr>
                      <td>
                        <label for={0}>{0}</label>
                      </td>
                      <td>
                        <input type="{1}" name="{0}"/>
                      </td>
                    </tr>
                    """.format(form_label, form_type) + error_span

        # Add form_table_elements to signup_form html
        signup_form =  "<form action='/welcome' method='post'><table>"+ form_table_elements + "</table><input type='submit' value='Submit'/>"

        # Put the page together and then write
        content = page_header + index_header + signup_form + page_footer
        self.response.write(content)

class WelcomeHandler(webapp2.RequestHandler):
    """
    Handles form post to /welcome;
    Verify all user inputs
    """
    def post(self):
        # look inside the request to figure out what the user typed
        username = self.request.get("Username")
        password = self.request.get("Password")
        verify = self.request.get("verify")
        email = self.request.get("email")

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

        #If all tests successful, get username and send greeting
        else:
            welcome_message = "<h2>Welcome, " + username + "</h2>"
            content = page_header + welcome_message + page_footer
            self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', WelcomeHandler)
], debug=True)
