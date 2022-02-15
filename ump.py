#!/usr/bin/env python3

import logging
import logging.handlers
import rich
import configparser
import imaplib

from rich.console import Console
from rich.logging  import RichHandler
#from rich.progress import track
from rich.pretty import pprint
#from rich import inspect
#from rich import print
import rich.traceback

import umplib.message

########################################## Initialisations globales
rich.traceback.install()
log = logging.getLogger("ump")
console = Console()

if __name__ == "__main__":

    logging.basicConfig(
        handlers=[RichHandler(rich_tracebacks=True)])
    log.setLevel(logging.DEBUG)

    ini = configparser.ConfigParser()
    ini.read('ump-secret.ini')

    imap_server = ini['imap']['server']
    imap_port = ini['imap']['port']
    imap_user=ini['imap']['login']
    imap_password=ini['imap']['password']



    log.debug("connexion <"+imap_server +":" +str(imap_port)+ "> ")

    try:
        with imaplib.IMAP4_SSL(host=imap_server, port=imap_port, ) as imap:
            log.debug("connected")
            imap.login(imap_user,imap_password)
            imap.select()
            log.debug("logged in")

            ret, data = imap.uid('search', None, '(UNSEEN)')
            if ret != 'OK':
                raise Exception("Failed to search for unseen messages")
            uids = data[0].split()
            if len(uids) != 0 :
                messages = []
                for uid in uids:
                    log.debug("fetching message "+str(uid))
                    ret, data = imap.uid('fetch', uid, '(BODY[TEXT])')
                    if ret == 'OK':
                        body = data[0][1]
                    messages.append( umplib.message.Message( str(body)) )
                for msg in messages:
                    log.info( msg.DSNs )    
            else:
                log.info("no unread message")
    except:
        log.exception("problem with IMAP server")
        exit(1)
    log.info("done.")



