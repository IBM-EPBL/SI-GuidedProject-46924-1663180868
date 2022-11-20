import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# sendgrid integration
def mailtest_registration():
    message = Mail(
    from_email='rushal1218prem@gmail.com',
    to_emails= 'mprem2616@gmail.com',
    subject='Registration Successfull!',
    html_content='<strong>You have successfully registered as user. Please Login using your Username and Password to donate/request for Plasma.</strong>')
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
    
