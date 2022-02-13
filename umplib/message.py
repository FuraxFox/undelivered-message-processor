import email

class Message :
    
    def __init__(self, msgstr):
        self.DSNs = []
        self.orig_msg = None

        msg = email.message_from_string( msgstr )
        if (msg.is_multipart() and len(msg.get_payload()) > 1 and 
            msg.get_payload(1).get_content_type() == 'message/delivery-status'):
            
            for dsn in msg.get_payload(1).get_payload():
                self.DSNs.append(dsn)
        
            if len(msg.get_payload()) > 2:
                self.orig_msg= msg.get_payload(2) # original message

    def DSNs( self ):
        return self.DSNs

    
