import base64
import os
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
try:
    # Python 3
    import urllib.request as urllib
except ImportError:
    # Python 2
    import urllib2 as urllib

import os
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def sendemail():
	message = Mail(
		from_email='yw996@cornell.edu',
		to_emails='yanlingwu95@gmail.com',
		subject='The prediction result',
		html_content='<strong>We only show the prediction results that the cow might not be pregnancy!! Details with attachment! </strong>')
	file_path = 'pre_result.txt'
	with open(file_path, 'rb') as f:
		data = f.read()
		f.close()
	encoded = base64.b64encode(data).decode()
	attachment = Attachment()
	attachment.file_content = FileContent(encoded)
	attachment.file_type = FileType('application/txt')
	attachment.file_name = FileName('pre_result.txt')
	attachment.disposition = Disposition('attachment')
	attachment.content_id = ContentId('Example Content ID')
	message.attachment = attachment
	try:
		sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
		response = sendgrid_client.send(message)
		print(response.status_code)
		print(response.body)
		print(response.headers)
	except Exception as e:
		print(e.message)
