#!/usr/bin/python3

import imaplib
#import umplib.message

from imaplib import IMAP4

import logging
import logging.handlers
import rich
import configparser

from rich.console import Console
from rich.logging  import RichHandler
#from rich.progress import track
from rich.pretty import pprint
#from rich import inspect
#from rich import print
import rich.traceback

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
            for uid in uids:
                log.debug("fetching message "+str(uid))
                ret, data = imap.uid('fetch', uid, '(BODY[TEXT])')
                if ret == 'OK':
                    body = data[0][1]
    except:
        log.exception("problem with IMAP server")



