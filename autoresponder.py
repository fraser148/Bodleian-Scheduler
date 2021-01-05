#import sys
import json
from urllib.request import Request#, urlopen
import urllib
import imaplib
import smtplib
import logging
#import getpass
import email
import email.header
import time
import datetime
from random import randint
#from email.message import EmailMessage
#from ics import Calendar, Event
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate#, COMMASPACE

sender_of_interest = 'fjrennie1@outlook.com'

def new_email():
    global smtp

    send_from = "bodleian.scheduler@oxtickets.co.uk"
    send_to = "fraser.rennie@exeter.ox.ac.uk"
    subject = "BOD SLOT"
    text = "Hi Fraser,\n\nYour slot is attached as an .ics file\n\nKind Regards,\nFraser Rennie"

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    f = "my.ics"
    fil = open(f, 'rb')
    part = MIMEApplication(fil.read(),Name=basename(f))
    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
    msg.attach(part)
    smtp.sendmail(send_from, send_to, msg.as_string())

def new_email2(start, end, library, account):
    global smtp
    CRLF = "\r\n"
    attendees = [account]
    organizer = "ORGANIZER;CN=Bodleian Scheduler:mailto:bodleian.scheduler"+CRLF+" @oxtickets.co.uk"
    fro = "Bodleian Scheduler <bodleian.scheduler@oxtickets.co.uk>"

    ddtstart = datetime.datetime.now()
    dtoff = datetime.timedelta(days = 1)
    dur = datetime.timedelta(hours = 1)
    ddtstart = ddtstart +dtoff
    dtend = ddtstart + dur
    dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    dtstart = ddtstart.strftime("%Y%m%dT%H%M%SZ")
    starter = start.strftime("%Y%m%dT%H%M%SZ")
    ender = end.strftime("%Y%m%dT%H%M%SZ")
    print(dtstart)
    dtend = dtend.strftime("%Y%m%dT%H%M%SZ")

    description = "DESCRIPTION: Bodleian Library Slot"+CRLF
    attendee = ""
    for att in attendees:
        attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+att+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+att+CRLF
    ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:pyICSParser"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
    #ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
    ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+starter+CRLF+"DTEND:"+ender+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
    ical+= "UID:FIXMEUID"+dtstamp+str(randint(1000, 9999))+CRLF
    ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
    #ical+= "SUMMARY:test "+ddtstart.strftime("%Y%m%d @ %H:%M")+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF
    ical+= "SUMMARY:"+library+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF

    eml_body = "Your slot is in: " + library + "\n\n" + start.strftime("%d/%m/%Y @ %H:%M")
    #eml_body_bin = "This is the email body in binary - two steps"
    msg = MIMEMultipart('mixed')
    msg['Reply-To']=fro
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = library
    msg['From'] = fro
    msg['To'] = ",".join(attendees)

    part_email = MIMEText(eml_body,"html")
    part_cal = MIMEText(ical,'calendar;method=REQUEST')

    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)

    ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
    ical_atch.set_payload(ical)
    encoders.encode_base64(ical_atch)
    ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))

    eml_atch = MIMEBase('text/plain','')
    #encoders.encode_base64(eml_atch)
    eml_atch.add_header('Content-Transfer-Encoding', "")

    msgAlternative.attach(part_email)
    msgAlternative.attach(part_cal)

    smtp.sendmail(fro, attendees, msg.as_string())


def get_details(body):
    start = body.find('starts at:')
    start = body.split("starts at:",1)[1]
    start = start.split("\n",1)[0].lstrip()

    end = body.find('ends at:')
    end = body.split("ends at:",1)[1]
    end = end.split("\n",1)[0].lstrip()

    #library = body.find("as follows:")
    library = body.split("as follows:",1)[1].lstrip()
    library = library.split("\n",1)[0].lstrip()

    return start, end, library

def format_date(date):
    DD = date[0:2]
    MM = date[3:5]
    YYYY = date[6:10]
    HH = date[11:13]
    mm = date[14:16]

    normal_date = YYYY + "-" + MM + "-" + DD + " " + HH + ":" + mm
    new_date = datetime.datetime.strptime(normal_date, '%Y-%m-%d %H:%M')
    print(new_date)
    return new_date

def process_mailbox(M, account):
    """
    Do something with emails messages in the folder.  
    For the sake of this example, print some headers.
    """

    #rv, data = M.search(None, "ALL")
    try:
        rv, data = M.search(None, '(UNSEEN)', '(FROM "%s")' % (account))
        if rv != 'OK':
            print("No messages found!")
            return

        for num in data[0].split():
            rv, data = M.fetch(num, '(RFC822)')
            if rv != 'OK':
                print("ERROR getting message", num)
                return
            # Mark messages as read
            #M.store(num, '+FLAGS', '(SEEN)')

            msg = email.message_from_bytes(data[0][1])
            hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
            if "Declined" in str(hdr):
                print("Denied appointment")
            elif "Accepted" in str(hdr):
                print("Accepted appointment")
            elif "Booking Confirmation" in str(hdr):
                subject = str(hdr)
                print('Message %s: %s' % (num, subject))
                body = msg.get_payload(0)
                body = body.get_payload()
                start, end, library = get_details(body)
                print(library)
                print('Start Time')
                print(start)
                print('End Time')
                print(end)
                start = format_date(start)
                end = format_date(end)
                new_email2(start, end, library, account)
                # Now convert to local date-time
                date_tuple = email.utils.parsedate_tz(msg['Date'])
                if date_tuple:
                    local_date = datetime.datetime.fromtimestamp(
                        email.utils.mktime_tz(date_tuple))
                    print ("Local Date:", \
                        local_date.strftime("%a, %d %b %Y %H:%M:%S"))
            else:
                print("invalid email")
    except:
        print("connection Error")
        logging.warning('There was a connection error')

counter = 60

logging.basicConfig(filename='errors.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

while 1:
    try:
        # Newline
        imap = imaplib.IMAP4_SSL('mail.oxtickets.co.uk', '993')
        imap.login('bodleian.scheduler@oxtickets.co.uk', 'DougFas224!')
        imap.select('Inbox')
        smtp = smtplib.SMTP_SSL('mail.oxtickets.co.uk', 465)
        smtp.ehlo()
        smtp.login('bodleian.scheduler@oxtickets.co.uk', 'DougFas224!')
        
    except:
        print("something went wrong - Login")
        logging.warning('Something went wrong in the login')
        continue

    # go through all unseen and then check whether in list

    if counter == 60:
        try:
            print("CHECKING ACCOUTNS")

            counter = 0
            #f= open("http://scheduler.oxtickets.co.uk/StudentsData.json")
            urler = Request("http://oxtickets.co.uk/StudentsData.json", headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(urler) as url:
                prueba = json.loads(url.read().decode())

            #prueba = json.load(f)
            accounts = [] # your list with json objects (dicts)
            


            for item in prueba:
                accounts.append(item['Email'])
            
            print(accounts)
        except:
            print("There was an error reading the accounts to check")
            logging.warning('There was an error reading the accounts to check')

    for account in accounts:
        try:
            process_mailbox(imap, account)
        except:
            print("There was an error")
            logging.warning('There was an error when trying to read the mailboxes')
    try:
        imap.logout()
        smtp.close()
        time.sleep(1)
        counter += 1
    except:
        print("Failed to log out")
        logging.warning('Failed to log out')

