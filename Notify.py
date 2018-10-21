import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '
# Define params
rrdpath = '/home/cabogabo/PycharmProjects/observatoriumPantitlan/bdrrdtool/'
pngpath = '/home/cabogabo/PycharmProjects/observatoriumPantitlan/graficas/'
fname = 'gCPU.rrd'
fname1 = 'gRAM.rrd'
width = '500'
height = '200'
mailsender = "observatoriumpantitlan@gmail.com"
#mailreceip = "gabo.alejandro.huitron@gmail.com"
mailreceip = "observatoriumpantitlan@gmail.com"
mailserver = 'smtp.gmail.com: 587'
password = 'observatorium1234'

def send_alert_attached(subject, tipo):
    """ Will send e-mail, attaching png
    files in the flist.
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = mailreceip
    if(tipo=="CPU"):
        fp = open(pngpath+'gCPU.png', 'rb')
    elif(tipo=="RAM"):
        fp = open(pngpath+'gRAM.png', 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)
    mserver = smtplib.SMTP(mailserver)
    mserver.starttls()
    # Login Credentials for sending the mail
    mserver.login(mailsender, password)

    mserver.sendmail(mailsender, mailreceip, msg.as_string())
    mserver.quit()
