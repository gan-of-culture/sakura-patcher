#!/usr/bin/python
#
# Download WeTransfer files
#
# VERSION   : v1.1
# DATE      : 15th September 2020
# AUTHOR    : Gary Watson <https://github.com/GaryWatsonUK>
# URL       : https://github.com/GaryWatsonUK/py-wetransfer
# DEPENDS   : pip install requests ; pip install HTMLParser (Python 3.x only)

import getopt
import json
import os
import requests
import sys

if (sys.version_info > (3, 0)):
    from urllib.parse import urlparse, parse_qs
    from html.parser import HTMLParser
else:
    from urlparse import urlparse, parse_qs
    from HTMLParser import HTMLParser

class HTMLMetaTagCSRFTokenParser(HTMLParser):
    def __init__(self):
        # Python 3 requires a call to super().__init__()
        if (sys.version_info > (3, 0)): super().__init__()
        self.reset()
        self.CSRF_Token = ''
    def handle_starttag(self, tag, attrs):
        if "meta" in tag:
            if len(attrs) == 2:
                (key, value) = attrs[0]
                if key == 'name' and value == 'csrf-token':
                    (tokenKey, tokenValue) = attrs[1]
                    if tokenKey == 'content':
                        self.CSRF_Token = tokenValue
    def clean(self):
        self.CSRF_Token = ''

class HTMLDataParser(HTMLParser):
    def __init__(self):
        # Python 3 requires a call to super().__init__()
        if (sys.version_info > (3, 0)): super().__init__()
        self.reset()
        self.HTMLData = []
    def handle_data(self, data):
        self.HTMLData.append(data)
    def clean(self):
        self.HTMLData = []

def main(argv):
    try:
        url = argv
        with requests.Session() as session:
            responseData = perform_get_from_url(url, session)

            # If the shortened URL was used, then get the full URL from the response headers
            if len(responseData.text) == 0 and len(responseData.headers['location']) > 0:
                url = responseData.headers['location']

            [file_id, recipient_id, security_hash] = extract_params(url)

            requestData = session.get(url)

            domain_user_id = extract_domain_user_id(requestData.text)

            csrf_token = extract_csrf_token(requestData.text)

            download_link = extract_direct_download_link(session, file_id, recipient_id, security_hash, domain_user_id, csrf_token)
            
            if len(download_link) > 0:
                perform_download(download_link)
                
                return 0
            else:
                print("Could not extract the direct download link")
                sys.exit(1)

    except requests.exceptions.HTTPError as e:
        if len(e.args) == 1 and e.args[0].startswith("417"):
            print("Please check the request.  The data in the response from WeTransfer may have changed. ('417 Client Error : Expectation Failed')")
        else:
            print("general HTTPError occurred:\n{0} (args:{1!r})".format(type(e).__name__, e.args))

        sys.exit(1)

    except KeyboardInterrupt as e:
        print("\n\nUser interrupted the download - aborted")
        sys.exit(1)

    except getopt.GetoptError:
        sys.exit(2)

def display_usage():
    print("""
You should have a We transfer address similar to https://www.wetransfer.com/downloads/XXXXXXXXXX/YYYYYYYYY or https://we.tl/XXXXXXXXXXXX

So execute:

python wetransfer.py https://we.tl/XXXXXXXXXXXX

And download it! :)
""")
    sys.exit()

def extract_csrf_token(htmlData):
    """
        Uses a HTMLParser to locate and return a required token
    """
    parsedHTML = HTMLMetaTagCSRFTokenParser()
    parsedHTML.feed(htmlData)

    token = parsedHTML.CSRF_Token

    parsedHTML.clean()

    return token

def extract_direct_download_link(session, file_id, recipient_id, security_hash, domain_user_id, csrf_token):
    """
        Calls the API in order to retrieve the direct link
    """
    url = "https://wetransfer.com/api/v4/transfers/{0}/download".format(file_id)

    headers = {"x-csrf-token": csrf_token}

    body = {"security_hash": security_hash, "intent": "entire_transfer", "domain_user_id": domain_user_id}

    r = session.post(url, json=body, headers=headers)

    r.raise_for_status()
    
    jsonData = r.json()

    if 'direct_link' in jsonData:
        return jsonData['direct_link']

def extract_domain_user_id(htmlData):
    """
        Extracts the required domain_user_id value from the HTML
    """
    parsedHTML = HTMLDataParser()
    parsedHTML.feed(htmlData)

    data = parsedHTML.HTMLData

    parsedHTML.clean()

    for index, value in enumerate(data):
        if "__launch_darkly" in value and "feature_flags" in value:
            firstPos = value.find('{')
            lastPos = value.rfind('}')
            extracted = value[firstPos:lastPos]
            obj = extracted.split()

            for idx, val in enumerate(obj):
                if 'user:' in val:
                    keyData = obj[idx+1]
                    jsonData = json.loads(keyData)
                    return jsonData['key']

def extract_params(url):
    """
            Extracts params from url
    """
    params = url.split("downloads/")

    file_id = ""
    recipient_id = ""
    security_hash = ""

    if len(params) > 0:
        [file_id, recipient_id, security_hash] = ['', '', '']

        if "http" in params[0]:
            parts = params[1].split('/')
            [file_id, security_hash] = parts
        else:
            if len(parts) > 2:
                # The url is similar to
                # https://www.wetransfer.com/downloads/XXXXXXXXXX/YYYYYYYYY/ZZZZZZZZ
                [file_id, recipient_id, security_hash] = params
            else:
                # The url is similar to https://www.wetransfer.com/downloads/XXXXXXXXXX/ZZZZZZZZ
                # In this case we have no recipient_id
                [file_id, security_hash] = parts
    else:
        print("no params")

    return [file_id, recipient_id, security_hash]

def perform_download(url, outdir=None):
    """
        Use the direct link URL to download the file
    """
    if outdir is None:
        outdir = os.getcwd()

    direct_link_path = urlparse(url).path
    path_parts = direct_link_path.split('/')
    file_name = path_parts[-1]

    output_full_path = os.path.join(outdir, file_name)

    r = requests.get(url, stream=True)
    
    file_size = int(r.headers["Content-Length"])
    
    print("Starting download of {0} to {1} (file size = {2} bytes)".format(file_name, output_full_path, file_size))
    
    output_file = open(output_full_path, 'wb')
    
    counter = 0
    chunksize = 1024
    previousPerCent = 0

    sys.stdout.write(
       '\n\r0% 0/{0}'.format(file_size)
    )
    sys.stdout.flush()

    for chunk in r.iter_content(chunk_size=chunksize):
        if chunk:
            output_file.write(chunk)
            output_file.flush()
            
            currentPercent = int((counter * chunksize) * 100 / file_size)

            if currentPercent > previousPerCent:
                previousPerCent = currentPercent
                
                sys.stdout.write(
                   '\r{0}% {1}/{2}'.format(currentPercent, counter * chunksize, file_size)
                )
                sys.stdout.flush()
            
            counter += 1

    output_file.close()

    sys.stdout.write('\r100% {0}/{1}\n'.format(file_size, file_size))

    print('\nCompleted downloading to {0}\n'.format(output_full_path))

def perform_get_from_url(url, session):
    return session.get(url, allow_redirects=False)
