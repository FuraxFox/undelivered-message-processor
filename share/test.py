
import email
from rich import print
from rich.pretty import pprint

msg = """
--05D02198038B.1644859448/mail.goupil.one
Content-Description: Delivery report
Content-Type: message/delivery-status

Reporting-MTA: dns; mail.goupil.one
X-Postfix-Queue-ID: 05D02198038B
X-Postfix-Sender: rfc822; crenard@goupilland.net
Arrival-Date: Mon, 14 Feb 2022 17:24:07 +0000 (UTC)

Final-Recipient: rfc822; nexistepas@goupilland.net
Original-Recipient: rfc822;nexistepas@goupilland.net
Action: failed
Status: 5.1.1
Diagnostic-Code: X-Postfix; unknown user: "nexistepas"
"""

print(msg)

res = []
for sub in msg.split("\n"):
    if ':' in sub:
        res.append(map(str.strip, sub.split(':', 1)))
res = dict(res)
pprint(res)
