#!/usr/bin/env python3

import argparse
import configparser
import csv
import imaplib
import logging
import re
import rich
import rich.console
import rich.traceback
import rich.logging  
import rich.progress 

import umplib.message


def dicts2csv(filename,DSNs):
    """
    Receive a list of DSN as dictionaries and write them to an Ms Excel compatible CSV file
    """
    headers = [
        'From',
        'To', 
        'Arrival-Date',
        'Action',
        'Status',
        'Diagnostic-Code',
        'Reporting-MTA',
        'Remote-MTA',
        'Received-From-MTA',        
        'Final-Recipient',
        'Message-ID'
        ]
    rows = []
    for dsn in DSNs:
        row = []
        for fld in headers:
            if fld in dsn.keys():
                val = dsn[fld]
                val = re.sub(";\s*",": ", val)                
            else:
                val =''            
            row.append( val )
        rows.append(row)
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(headers)
        for row in rows:
            csvwriter.writerow(row)
    

########################################## Main
if __name__ == "__main__":

    # logging, console, error handling inits
    rich.traceback.install()
    log = logging.getLogger("ump")
    console = rich.console.Console()
    logging.basicConfig(
        handlers=[ rich.logging.RichHandler(rich_tracebacks=True) ] )
    log.setLevel(logging.INFO)

    # parsing commande line
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="configuration file", default="ump-secret.ini")
    parser.add_argument("-o", "--output", help="destination file",   default="output.csv")
    args = parser.parse_args()
    csv_filename = args.output
    ini_filename = args.config

    # reading config
    try:
        ini = configparser.ConfigParser()
        ini.read(ini_filename)

        imap_server   = ini['imap']['server']
        imap_port     = ini['imap']['port']
        imap_user     = ini['imap']['login']
        imap_password = ini['imap']['password']
        imap_folder = 'INBOX'
        if 'folder' in ini['imap'].keys():
            imap_folder   = ini['imap']['folder']            
    except:
        log.exception("failed to read configuration from '"+ini_filename+"'")
        exit(1)

    log.info("checking "+imap_user+"@"+imap_server+" mailbox")
    log.debug("connexion <"+imap_server +":" +str(imap_port)+ "> ")
    
    try:
        # connecting to IMAPS server
        with imaplib.IMAP4_SSL( host=imap_server, port=imap_port ) as imap:
            log.debug("connected")
            imap.login( imap_user, imap_password )
            imap.select(imap_folder)
            log.debug("logged in")

            # getting UID list for unread messages 
            ret, data = imap.uid('search', None, '(UNSEEN)')
            if ret != 'OK':
                raise Exception("Failed to search for unseen messages")
            uid_list_str = data[0]
            uid_list = uid_list_str.split()
            if len(uid_list) != 0 :
                # there are some unread messages to process
                log.debug("processing messages")
                DSNs = []
                for uid in rich.progress.track(uid_list):
                    log.debug("fetching message " + str(uid) )
                    res1, data  = imap.uid( 'fetch', uid, '(RFC822)')
                    res2, flags = imap.uid( 'store', uid,'-FLAGS','\\Seen')
                    if res1 == 'OK':                    
                        # processing the message content    
                        msg = umplib.message.DSNMessage( data[0][1], logger=log )
                        if not msg.DSN() is None:
                            # we have a DSN
                            DSNs.append( msg.DSN() )
                    else:
                        log.warning("failed to get message uuid:" + uid + " : " + res1)
                log.info("Finished interrogating server, "+str(len(DSNs))+ " DSN found")

                log.info("saving data to '"+csv_filename+"'")
                dicts2csv(csv_filename, DSNs)
            else:
                log.info("no message to check")
    except:
        log.exception("problem with IMAP server")
        exit(1)

    log.info("done.")



