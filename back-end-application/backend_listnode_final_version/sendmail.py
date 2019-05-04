# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def sendemail(myMessage):
	message = Mail(
		from_email='yw996@cornell.edu',
		to_emails= 'yanlingwu95@gmail.com',
		subject='Pi might have issues, needing check!',
		html_content='<strong>'+ myMessage+'</strong>')
	try:
		sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
		response = sg.send(message)
		print(response.status_code)
		print(response.body)
		print(response.headers)
	except Exception as e:
		print(e.message)
