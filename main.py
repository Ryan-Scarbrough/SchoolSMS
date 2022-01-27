# Author: Ryan Scarbrough
# LE: 1/26/22
# THIS FILE DECIDES WHAT TO RESPOND WITH WHEN A MESSAGE IS RECEIVED

from getChapels import getData
from getAssignments import getAsgn
import login # login info
import time 
from datetime import datetime, timedelta
from twilio.rest import Client
from flask import Flask

app = Flask(__name__) 
@app.route('/sms', methods=['POST'])
def recieved():
    client = Client(login.acc_sid, login.auth_token) # logging in
    messages = client.messages.list(from_=login.phone_to,limit=20) # getting the messages
    time_recieved = messages[0].date_sent # getting the time the message was recieved
    message_body = messages[0].body # getting the message body
    return str(message_body), str(time_recieved) 

def text(msg):
    client = Client(login.acc_sid, login.auth_token) # logging in
    client.messages.create(from_=login.phone_from, body=msg, to=login.phone_to) # sending the message
    print('Message sent')

last_time = 0
previous_attend = 0
first = 0

while True:
    try:
        attend, left = getData() # two integers
        names, times = getAsgn() # two lists
    except:
        print('Request failed. Waiting 30s and trying again')
        time.sleep(30)
        continue

    # to keep original data
    orig_times = []
    for i in times:
        orig_times.append(i)
    
    # reformats date/time to: January 18 2022 11:59PM
    for i in range(len(times)):
        times[i] = times[i][:-1]
        a = times[i][:-3]
        b = times[i][-2:]
        times[i] = a + b
        times[i] = times[i].replace(',', '')

        # not fixing this
        if len(times[i].split(' ')[1]) == 1:
            times[i] = times[i].replace(times[i].split(' ')[1], '0' + times[i].split(' ')[1], 1)

        times[i] = datetime.strptime(times[i], '%B %d %Y %I:%M%p')
    
    # 24-hour text message for assignments
    to_text_24 = []
    for i in range(len(times)):
        if times[i] - datetime.now() < timedelta(hours=24) and times[i] - datetime.now() > timedelta(hours=23, minutes=55):
            to_text_24.append(names[i])
    for i in to_text_24:
        text(f"24 HOUR REMINDER:\n{i}")
    if len(to_text_24) > 0:
        time.sleep(300)

    # 12-hour text message for assignments
    to_text_12 = []
    for i in range(len(times)):
        if times[i] - datetime.now() < timedelta(hours=12) and times[i] - datetime.now() > timedelta(hours=11, minutes=55):
            to_text_12.append(names[i])
    for i in to_text_12:
        text(f"12 HOUR REMINDER:\n{i}")
    if len(to_text_12) > 0:
        time.sleep(300)

    # 6-hour text message for assignments
    to_text_6 = []
    for i in range(len(times)):
        if times[i] - datetime.now() < timedelta(hours=6) and times[i] - datetime.now() > timedelta(hours=5, minutes=55):
            to_text_6.append(names[i])
    for i in to_text_6:
        text(f"6 HOUR REMINDER:\n{i}")
    if len(to_text_6) > 0:
        time.sleep(300)

    try:
        msg, time_recieved = recieved()
        msg = msg.lower().strip()
    except:
        print('Something went wrong...')
        time.sleep(10)
        continue

    # 3-hour text message for assignments
    to_text_3 = []
    for i in range(len(times)):
        if times[i] - datetime.now() < timedelta(hours=3) and times[i] - datetime.now() > timedelta(hours=2, minutes=55):
            to_text_3.append(names[i])
    for i in to_text_3:
        text(f"3 HOUR ALERT:\n{i}")
    if len(to_text_3) > 0:
        time.sleep(300)

    try:
        msg, time_recieved = recieved()
        msg = msg.lower().strip()
    except:
        print('Something went wrong...')
        time.sleep(10)
        continue
    
    # chapel skips left
    skips = (int(left) - int(attend)) - 1 # the -1 is needed because the chapel data is not updated on covenant website when I query

    # decides what to say based on message
    if time_recieved != last_time and first != 0: # making sure we don't reply to the same message twice
        if 'hello' in msg or 'hi' in msg or 'hey' in msg:
            text('Hello :)')
        if 'chapels' in msg or 'chapel' in msg:
            text(f'There are {left} chapel(s) left; you must attend {attend} of them ({skips} skips left).')
        if 'test' in msg:
            text('Everything seems to be working fine')
        if 'assignment' in msg or 'assignments' in msg:
            for i in range(len(names)):
                text(f'{names[i]}\nDUE: {orig_times[i]}')
        if 'skips' in msg:
            text(f'You have {skips} left.')
        if 'help' in msg:
            text('Commands: "hello", "chapels", "test", "assignments", "skips"')
    
    last_time = time_recieved

    # chapel attendence logic
    if int(attend) < int(previous_attend) and first != 0:
        text(f'Nice, you recieved a chapel credit! You must attend {attend} more ({skips} skips left).')
    elif int(attend) > int(previous_attend) and first != 0:
        text('You lost a chapel credit! :bruh:')
    previous_attend = attend
    
    first = 1
    print('Finished a loop...')
