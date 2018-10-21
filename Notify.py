import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '
# Define params
rrdpath = '/home/francisco/Escritorio/OBSERVATORIUM/bdrrdtool/'
pngpath = '/home/francisco/Escritorio/OBSERVATORIUM/graficas/'
fname = 'gCPU.rrd'
fname1 = 'gRAM.rrd'
width = '500'
height = '200'
mailsender = "lmethod1234@gmail.com"
#mailreceip = "gabo.alejandro.huitron@gmail.com"
mailreceip = "lmethod1234@gmail.com"
mailserver = 'smtp.gmail.com: 587'
password = '.l.'

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

