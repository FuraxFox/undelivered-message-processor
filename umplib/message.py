import email
import email.utils
import time
import datetime


def _is_part_dsn(msg):
    if len(msg) <= 1:
        return False
    if msg[1].get_content_type() != 'message/delivery-status':
        return False
    return True

def _first_among_in(keys, values_dict ):
    """
    return the value associated with the first key present in values_dict
    """
    for k in keys:
        if k in values_dict:
            return values_dict[k]
    return None

def _smtp_timestamp_to_iso8601(stamp):
    #tm = time.mktime(email.utils.parsedate(stamp))
    #dt = datetime.datetime(tm)
    #return dt.isoformat()
    return stamp

def _parse_dsn(dsntext,defaults):
    res = []
    for sub in dsntext.split("\n"):
        if ':' in sub:
            res.append(map(str.strip, sub.split(':', 1)))
    res = dict(res)

    for d in defaults.keys():
        if not d in res:
            res[d] = defaults[d]

    sender     = _first_among_in( ['X-Postfix-Sender','From', 'Sender'], res ) 
    recipient  = _first_among_in( ['Original-Recipient', 'Final-Recipient'], res )
    message_id = _first_among_in( ['X-Original-Message-ID','X-Postfix-Queue-ID', 'final-log-id'], res )            
    res['Arrival-Date'] = _smtp_timestamp_to_iso8601(res['Arrival-Date'])
    res['To']         = str(recipient)
    res['From']       = str(sender)
    res['Message-ID'] = str(message_id)

    return res

class DSNMessage :
    """
    Minimal wrapper for DSN message
    """
    def __init__(self, msgbytes, logger=None):
        self._dsn = None
        self.orig_msg = None
        self.logger=logger
        self._parse_message(msgbytes)
    
    def _parse_message(self, msgbytes):
        msg = email.message_from_bytes( msgbytes )
        if msg.is_multipart() :
            meta = {}
            meta['From']= msg.get('From')
            meta['Arrival-Date'] = msg.get('Date')

            payload = msg.get_payload()
            if  _is_part_dsn( payload ):
                self.logger.debug("delivery status found")            
                part_num=0
                for part in payload:
                    content_type = part.get_content_type()
                    if content_type == 'message/delivery-status':
                        self.logger.debug(" DSN part("+str(part_num)+"):<<\n"+str(part)+"\n>>")
                        self._dsn = _parse_dsn( part.as_string(), meta ) #part.get_payload()
                    else:
                        self.logger.debug(" non DSN part("+str(part_num)+"):<"+content_type+">")
                    part_num=part_num+1
                if len( payload ) > 2 :
                    self.orig_msg= payload[2] # original message
        else: 
            self.logger.debug("not multipart")

    def DSN( self ):
        return self._dsn

    
