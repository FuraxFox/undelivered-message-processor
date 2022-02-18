import email


def _is_part_dsn(msg):
    if len(msg) <= 1:
        return False
    if msg[1].get_content_type() != 'message/delivery-status':
        return False
    return True

def _parse_dsn(dsntext):
    res = []
    for sub in dsntext.split("\n"):
        if ':' in sub:
            res.append(map(str.strip, sub.split(':', 1)))
    res = dict(res)
    return res

class DSNMessage :
    
    def __init__(self, msgbytes, logger=None):
        self._dsn = None
        self.orig_msg = None
        self.logger=logger
        self._parse_message(msgbytes)

    
    def _parse_message(self, msgbytes):
        msg = email.message_from_bytes( msgbytes )
        if msg.is_multipart() :
            payload = msg.get_payload()
            if  _is_part_dsn( payload ):
                self.logger.debug("delivery status found")            
                part_num=0
                for part in payload:
                    content_type = part.get_content_type()
                    if content_type == 'message/delivery-status':
                        self.logger.debug(" DSN part("+str(part_num)+"):<<\n"+str(part)+"\n>>")
                        self._dsn = _parse_dsn( part.as_string() ) #part.get_payload()
                    else:
                        self.logger.debug(" non DSN part("+str(part_num)+"):<"+content_type+">")
                    part_num=part_num+1
                if len( payload ) > 2 :
                    self.orig_msg= payload[2] # original message
        else: 
            self.logger.debug("not multipart")


    def DSN( self ):
        return self._dsn

    
