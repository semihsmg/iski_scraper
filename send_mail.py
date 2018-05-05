import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = '...@mail'
PASSWORD = '...'

send_to = '...@mail'


def send(message):
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()  # create a message

    # Prints out the message body for our sake
    # print(message)

    # setup the parameters of the message
    msg['From'] = MY_ADDRESS
    msg['To'] = send_to
    msg['Subject'] = "Su kesinti bildirisi!"

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg
    # Terminate the SMTP session and close the connection
    s.quit()
