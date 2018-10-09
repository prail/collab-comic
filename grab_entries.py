#!python3
import os, io, poplib
from email import parser
from PIL import Image
#config file for storing credentials
import config
#check for unconfigured username or password
if config.USERNAME == "" or config.PASSWORD == "":
    print("Uh Oh, you should probably configure the POP username and password.")
    exit(1)

#The major parts of code involving connection and attachment retrieval were taken
#from https://stackoverflow.com/a/30784602/ thanks torrange!
def connect(server,user,passwd):
    #connects to POP server
    conn = poplib.POP3_SSL(server)
    conn.user(user)
    conn.pass_(passwd)
    return conn

def fetch_mail(delete_after=False):
    #fetches mail in POP inbox
    conn = connect(config.SERVER,config.USERNAME,config.PASSWORD)
    messages = [conn.retr(i) for i in range(1, len(conn.list()[1]))]
    messages = ["\n".join(map(bytes.decode, mesg[1])) for mesg in messages]
    messages = [parser.Parser().parsestr(mesg) for mesg in messages]
    if delete_after == True:
        delete_messages = [conn.dele(i) for i in range(1, len(conn.list()[1]) + 1)]
    conn.quit()
    return messages

if not os.path.exists("./entries"):
    os.mkdir("./entries")
messages = fetch_mail()

i=0
for msg in messages:
    for part in msg.walk():
        if part.get_content_type() == "image/png": #only grab PNGs
            name = part.get_filename()
            data = part.get_payload(decode=True)
            f = io.BytesIO(data) # create fake file for PIL to load from
            img = Image.open(f)
            if img.size == (512,512): # only write correct dimensioned images
                i+=1
                img.save(f"./entries/{i:03d}.png","PNG") # save images named sequentially in entries dir
            img.close() # release all that memory
