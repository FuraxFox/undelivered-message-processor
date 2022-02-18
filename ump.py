#!/usr/bin/env python3

import logging
import logging.handlers
import rich
import configparser
import imaplib

from rich.console import Console
from rich.logging  import RichHandler
from rich.progress import track
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
        handlers=[ RichHandler(rich_tracebacks=True) ] )
    log.setLevel(logging.DEBUG)

    ini = configparser.ConfigParser()
    ini.read('ump-secret.ini')

    imap_server   = ini['imap']['server']
    imap_port     = ini['imap']['port']
    imap_user     = ini['imap']['login']
    imap_password = ini['imap']['password']

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
            uid_list_str = data[0]
            uid_list = uid_list_str.split()
            if len(uid_list) != 0 :
                log.debug("processing messages")
                messages = []
                for uid in track(uid_list):
                    log.debug("fetching message " + str(uid) )
                    res1, data  = imap.uid( 'fetch', uid, '(RFC822)')
                    res2, flags = imap.uid( 'store', uid,'-FLAGS','\\Seen')
                    if res1 == 'OK':
                        messages.append( 
                            umplib.message.Message( 
                                data[0][1], 
                                logger=log ) )
                    else:
                        log.warning("failed to get message uuid:" + uid + " : " + res1)
                log.debug("processing collected DSN")
                for msg in messages:
                    log.info("dsn: "+ str(msg.DSN()) )
            else:
                log.info("no unread message")
    except:
        log.exception("problem with IMAP server")
        exit(1)
    log.info("done.")



