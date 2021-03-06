from selenium import webdriver

# read in Gmail password from external file
with open('bradbot9000_gmail_pwd') as f:
	gmail_password = f.read()

driver = webdriver.PhantomJS()
driver.get("http://webapps.sftc.org/trafficPayment/trafficpayment.dll")

# search for citation
driver.find_element_by_name("CitationNum").send_keys("018413334")
driver.find_element_by_id("SearchBtn").click()

# check to see whether "citation not found" error message block is hidden from view
# and set email subject/message accordingly
s = driver.page_source
i = s.find('<div id="errorBlock" style="">')
if i>0:
	subject = 'Citation 018413334 not found.'
	message = 'You\'re good.'
else:
	subject = 'CITATION 018413334 FOUND'
	message = 'pay up son: http://webapps.sftc.org/trafficPayment/trafficpayment.dll'

def send_email(recipients,subject,message,format='text',attachments=[]):
    import smtplib
    from email.MIMEBase import MIMEBase
    from email.MIMEText import MIMEText
    from email.MIMEMultipart import MIMEMultipart
    from email import Encoders
    
    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = 'bradbot9000@gmail.com'
    msg['To'] = ','.join(recipients) if type(recipients) != str else recipients
    body = MIMEMultipart('alternative')
    if format == 'text':
        body.attach(MIMEText(message, 'plain'))
    elif format == 'html':
        body.attach(MIMEText(message, 'html'))
    msg.attach(body)

    # Attach files if necessary
    if type(attachments) == str:
        attachments = [attachments]
    for attachment in attachments:
        if attachment.find('doc') > 0:
            attachFile = MIMEBase('application', 'msword')
        elif attachment.find('pdf') > 0:
            attachFile = MIMEBase('application', 'pdf')
        else:
            attachFile = MIMEBase('application', 'octet-stream')

        attachFile.set_payload(open(attachment).read())

        Encoders.encode_base64(attachFile)
        cid = '1234'
        attachFile.add_header('Content-Disposition', 'inline')
        attachFile.add_header('Content-ID', '<%s>' % cid)
        msg.attach(attachFile)
    while True:
        try:
            # send email
            gmail_user = 'bradbot9000@gmail.com'
            gmail_pwd = gmail_password
            smtpserver = smtplib.SMTP("smtp.gmail.com:587")
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            smtpserver.login(gmail_user, gmail_pwd)
            smtpserver.sendmail('bradbot9000@gmail.com', recipients, msg.as_string())
            smtpserver.close()
            print 'Email Sent: %s' % recipients
            break
        except Exception, e:
            print 'ERROR: Pausing for 3 minutes'
            print '\t %s' % e
            from time import sleep
            sleep(180)

send_email(['bradhd@gmail.com','bradbot9000@gmail.com'],subject,message)
