# undelivered-message-processor
A small script to process SMTP delivery reports

## Options

```
ump.py [-h] [-c CONFIG] [-o OUTPUT]
```

optional arguments:
```
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        configuration file
  -o OUTPUT, --output OUTPUT
                        destination file
```


## Configuration

```ini

[imap]
server=YourServerFQDN
port=YourServerPort
login=YourLoginHere
password=YourPasswordHere
folder=INBOX

`̀``


