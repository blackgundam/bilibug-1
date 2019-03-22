from google.appengine.api import mail

mail.send_mail(sender="blackgundamwyr@gmail.com",
                   to="Albert Johnson <wyr629@hotmail.com>",
                   subject="Your account has been approved",
                   body="""Dear Albert:

Your example.com account has been approved.  You can now visit
http://www.example.com/ and sign in using your Google Account to
access new features.

Please let us know if you have any questions.

The example.com Team
""")
