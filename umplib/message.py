import email

class Message :
    
    def __init__(self, msgbytes, logger=None):
        self.DSNs = []
        self.orig_msg = None
        self.logger=logger
        self._parse_message(msgbytes)

    
    def _parse_message(self, msgbytes):
        msg = email.message_from_bytes( msgbytes )
        if msg.is_multipart() :
            payload = msg.get_payload()
            if len(payload) > 1 and payload[1].get_content_type() == 'message/delivery-status' :
                self.logger.debug("delivery status found")            
                for dsn in msg.get_payload(1).get_payload():
                    self.DSNs.append(dsn)
                    self.logger.debug("DSN:"+str(dsn))

                if len(msg.get_payload()) > 2 :
                    self.orig_msg= payload[2] # original message
        else: 
            self.logger.debug("not multipart")


    def DSNs( self ):
        return self.DSNs

    
