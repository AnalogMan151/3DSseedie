#!/usr/bin/env python3
from urllib.parse import urlparse, urlencode
from urllib.error import HTTPError

import binascii
import urllib.request
import ssl
import sys

CA = '''-----BEGIN CERTIFICATE-----
MIIErDCCA5SgAwIBAgIBATANBgkqhkiG9w0BAQsFADCBmjELMAkGA1UEBhMCVVMx
EzARBgNVBAgTCldhc2hpbmd0b24xIjAgBgNVBAoTGU5pbnRlbmRvIG9mIEFtZXJp
Y2EsIEluYy4xCzAJBgNVBAsTAklTMSEwHwYDVQQDExhOaW50ZW5kbyBDbGFzcyAy
IENBIC0gRzMxIjAgBgkqhkiG9w0BCQEWE2NhQG5vYS5uaW50ZW5kby5jb20wHhcN
MTAwNDI5MTU1OTE4WhcNNDkxMjI4MTIwMDAwWjCBmjELMAkGA1UEBhMCVVMxEzAR
BgNVBAgTCldhc2hpbmd0b24xIjAgBgNVBAoTGU5pbnRlbmRvIG9mIEFtZXJpY2Es
IEluYy4xCzAJBgNVBAsTAklTMSEwHwYDVQQDExhOaW50ZW5kbyBDbGFzcyAyIENB
IC0gRzMxIjAgBgkqhkiG9w0BCQEWE2NhQG5vYS5uaW50ZW5kby5jb20wggEiMA0G
CSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDR0JlLuTabiKUVeaW1znP7dJ3m2vcu
SQk3QKAJf6inQREJIMG8LknTvdvX5Lmiwxd2P5hiSzmCzQyxMWN38zpQKzlW92es
FdwBnuUH9pXMDZBCcBEiwg2PxqNw4WdxlmRZ92R4g0Keenwh2GiETA2Ml2rasCCW
39TYNW7i8W0YQw7u1ZaMQ1GetWrvblt9UhmC7ZbI0pqJcBOZzR0tNbl79QT2WF8r
bRsSANlRi/H4LnjkMxrKrRYybLEfjDGBBfubhENKPRjUBEmp55gE2v0sVkLNLh2H
awCuSl+dpEG0D6BB/6/wZxxQdSbGVT6ahQRlHOVn0GZm4QC+Sc5yFYthAgMBAAGj
gfowgfcwHQYDVR0OBBYEFPfGCnxyfCzEvJMoQeTucPADoLu3MIHHBgNVHSMEgb8w
gbyAFPfGCnxyfCzEvJMoQeTucPADoLu3oYGgpIGdMIGaMQswCQYDVQQGEwJVUzET
MBEGA1UECBMKV2FzaGluZ3RvbjEiMCAGA1UEChMZTmludGVuZG8gb2YgQW1lcmlj
YSwgSW5jLjELMAkGA1UECxMCSVMxITAfBgNVBAMTGE5pbnRlbmRvIENsYXNzIDIg
Q0EgLSBHMzEiMCAGCSqGSIb3DQEJARYTY2FAbm9hLm5pbnRlbmRvLmNvbYIBATAM
BgNVHRMEBTADAQH/MA0GCSqGSIb3DQEBCwUAA4IBAQBE8V5A4HX/B3D2pbterUv8
P1hYXvF+qXXRLzEEmYSYDEC6eC/6biw1GmU1xamiuwzZC/1Llqv/9tUOsRiqbCcZ
y6PoplpfuoJpmoQltuP+hibDk6jSadEH1eK94P/6EnNpRHrgk5z4QVuXLmTi8iM6
7T5cVtqgXGhTOka6/AquzjrnJZA7q6OjH7soy+Ap4GW5iO3oNbfMcYWT25qVzhgV
cmm6niKF7yQY59H/XOaPOsL/fZlCRkp+UUxg/yj3bo+A34VSW8xlCu87HlVkKwlJ
4k5aF4MhHCbunoBTYwGhRC0hIlyvzIzG+Ky56UOimnZwztfJxA91uZzKPkWy5s43
-----END CERTIFICATE-----'''
URL_TEMPLATE = 'https://kagiya-ctr.cdn.nintendo.net/title/0x%016lx/ext_key' \
        + '?country=%s'
REGIONS = ('JP', 'US', 'GB', 'TW', 'KR', 'HK', 'DE', 'FR', 'ES', 'NL', 'IT', 'AU')

def main(argc, argv):
    if argc < 2:
        print("Usage: %s title_id" % argv[0])
        return 1
    try:
        title_id = int(argv[1], 16)
    except ValueError:
        print("Invalid title ID %s" % argv[1])
        return 1
    for region in REGIONS:
        req = urllib.request.Request(URL_TEMPLATE % (title_id, region),
                # s/P/D/ for dev
                # did not check if this is the correct UA
                headers={'User-Agent': 'CTR/P/1.0.0/r61631'})
        sslctx = ssl.create_default_context(cadata=CA)
        try:
            with urllib.request.urlopen(req, context=sslctx) as res:
                code = res.getcode()
                print(binascii.hexlify(res.read()).decode('ascii'))
                return 0
        except HTTPError as e:
            pass
    print("No seed for title %016lx." % title_id)

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
