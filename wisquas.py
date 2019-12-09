#!/usr/bin/python
import tldextract
from urlparse import urlparse
import sys
import requests
import socket
from pprint import pprint
import os
import urllib3
from colorama import Fore, Back, Style
import base64
import binascii
import codecs
import ssl
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl.match_hostname = lambda cert, hostname: True # Blocks error where IPs aren't matched to hosts of cert
cookie_lib = []

def helpme():
    print ('\nWisQuas (Reveal) - Example usage:\n')
    print ("Using 'Desktop Browser' profile...")
    print ("./wisquas-v1.py -1 'https://www.domain.com/dir1/dir2/otherstuff/'\n")
    print ("Using 'Mobile Browser' profile...")
    print ("./wisquas-v1.py -2 'https://www.domain.com/dir1/dir2/otherstuff/'")
    sys.exit()


def isEncoded(k):
    try:
        k = k.replace("%3D", "=")
        k = k.replace("%20", "+")
        k = k.replace("%2F", "/")
        k = k.strip("Basic ")
        #k = k.strip("Bearer ")
        all_strings = []
        new_strings = []
        final_strings = []
        k0 = k
        #all_strings.append(k0)
        strings = ['?','|','_',':',';',"';",'**',"'",'--','-','&','%3D',' ','~','\\','/','//','$','+','=','==',',','.',"**","*",'-']
        for p in strings:
            k1 = k.split(p)
            for all in k1:
                if all > 1:
                    all_strings.append(all)
                z = 0
                for more in all_strings:
                    while z < 2:
                        for p in strings:
                            k2 = more.split(p)
                            for last in k2:
                                #z = z + 1
                                if last > 1:
                                    all_strings.append(last)
                            z = z + 1
        all_strings2 = set(all_strings)
        for asdf in all_strings2:
            asdf = asdf.strip('"')
            try:
                decode_val3= codecs.decode(asdf, "hex")
                if asdf != "":
                    print Fore.GREEN + Style.DIM + "\nOriginal HEX string: " + asdf + Style.RESET_ALL
                    print Fore.GREEN + Style.BRIGHT + "Decoded HEX string: " + decode_val3 + Style.RESET_ALL
                    print "----------"
            except:
                pass
            try:
                try:
                    decode_val4 = base64.b64decode(asdf).decode("utf-8").rstrip('\n')
                except:
                    asdf = asdf + "=="
                    decode_val4 = base64.b64decode(asdf).decode("utf-8").rstrip('\n')
                if asdf != "":
                    print Fore.GREEN + Style.DIM + "\nOriginal B64 string: " + asdf + Style.RESET_ALL
                    print Fore.GREEN + Style.BRIGHT + "Decoded B64 string: " + decode_val4 + Style.RESET_ALL
                    print "----------"
            except:
                pass
        print Style.RESET_ALL
    except:
        pass
        print Style.RESET_ALL



def generate_https_connection(target,port):
    try:
        if target[-1:] == ".":
            target = target[:-1]
        context = ssl.create_default_context()
        scon = context.wrap_socket(socket.socket(), server_hostname=target)
        scon.connect((target, 443))
        cert = scon.getpeercert()
        cipher = scon.cipher()
        try:
            print "Cipher Used:"
            for a in cipher:
                print a,
            print "\n"
        except:
            pass
            print "no info\n"
        try:
            print "Subject:"
            subj = dict(x[0] for x in cert['subject'])
            print subj['organizationName'] + " | ",
            print subj['commonName'] + " | ",
            print subj['localityName'] + " | ",
            print subj['stateOrProvinceName'] + " | ",
            print subj['countryName'] + "\n"
        except:
            pass
            print "no info\n"
        try:
            print "Issued To:"
            print subj['commonName'] + "\n"
            print "Issuer:"
            issuer = dict(x[0] for x in cert['issuer'])
            print issuer['organizationName'] + " | ",
            print subj['commonName'] + " | ",
            print subj['countryName'] + "\n"
        except:
            pass
            print "no info\n"
        try:
            print "Valid Between:"
            not_after = cert.get('notAfter')
            not_before = cert.get('notBefore')
            print "Begin: " , not_before
            print "End:  " , not_after
        except:
            pass
            print "no info\n"
        print "\n" + Style.RESET_ALL
    except:
        pass
        print "SSL CERT ISSUE!!!!\n" + Style.RESET_ALL



try:
    url = sys.argv[2]
except:
    helpme()

'''
if url[-1:] != "/":
    url = url + "/"
'''

agent = sys.argv[1]

if agent not in ["-1","-2"]:
    helpme()


try:
    custom_host_header = sys.argv[3]
except:
    pass


print (Fore.GREEN + Style.BRIGHT + "\n")
print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
print("-   Wis Quas (v0.7) - Level 6 - REVEAL  -")
print("-    http://github.com/LostRabbitLabs   -")
print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n")

if agent == "-1":
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'
    }
    print "Using 'Desktop Browser' profile for crawling..."
    print "=============================================================="  + Style.RESET_ALL
else:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid Build/FRG22D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'
    }
    print "Using 'Mobile Browser' profile for crawling..."
    print "=============================================================="  + Style.RESET_ALL

try:
    if custom_host_header:
        headers.update({'Host': custom_host_header})
except:
    pass

o = urlparse(url)
host = tldextract.extract(o.netloc)
hostname = tldextract.extract(o.netloc)
domainname = host.domain + "." + host.suffix
hostname2 = hostname.subdomain + "." + domainname
hosts = str(hostname2)
proto = o.scheme

try:
    port = o.netloc.split(":")[1]
except:
    if proto == "http":
        port = 80
    elif proto == "https":
        port  = 443
    pass


if hosts[0] == ".":
    hosts = hosts[1:]

if hosts == 'localhost.':
    hosts = 'localhost'

try: # Checks for DNS query first, then switches to an IP query
    host_ip = socket.gethostbyname(hosts)
except:
    host_ip = domainname

try:
    asnresponse_host = requests.get('http://ipinfo.io/' + host_ip)
    asnresponse_host.json()
except:
    pass

print (Fore.WHITE + Style.BRIGHT)
print("Target URL:")
print(url + "\n")

print("Target Hostname:")
print(hosts + "\n")

print("Target Domain:")
print(domainname + "\n")

print("Target IP Address:")
print(host_ip + "\n\n")

print("ASN Information:")
print "=============================================================="
try:
    print asnresponse_host.json()['org']
    print asnresponse_host.json()['city'], ",", asnresponse_host.json()['region'], ",", asnresponse_host.json()['country'], asnresponse_host.json()['postal']
    print asnresponse_host.json()['timezone'], "-", asnresponse_host.json()['loc']
    print("\n")
except:
    print "problem with ASN lookup\n"

if proto == "https":
    print Fore.CYAN + Style.BRIGHT + "SSL Certificate Information:"
    print "=============================================================="
    generate_https_connection(domainname,port)

session = requests.Session()

try:
    response = session.get(url, verify=False, headers=headers, timeout=5)
    all_cookies = session.cookies.get_dict()
    all_headers = response.headers
    responsecode = response.status_code
    responsecode = str(responsecode)
    try:
        server = all_headers['Server']
    except:
        pass
        server = '--'
except:
    pass
    all_cookies = ""
    all_headers = ""

responsecontentlen = str(len(response.content))
total_cookies = str(len(all_cookies))
total_headers = str(len(all_headers))

print "Total Cookies: " + total_cookies
print "=============================================================="
for mycookies in all_cookies:
    cookievalue = all_cookies[mycookies]
    cookievalue = str(cookievalue)
    output = mycookies + " :: " + cookievalue
    print output
    #print "Checking for Base64 encoding of cookie: " , mycookies
    if len(cookievalue) > 5:
        #check1 = isBase64(cookievalue)
        #check2 = isHex(cookievalue)
        check1 = isEncoded(cookievalue)

print "\n"

print "Total Headers: " + total_headers
print "=============================================================="
for myheaders in all_headers:
    headersvalue = all_headers[myheaders]
    output2 = myheaders + " :: " + headersvalue
    print output2
    #print "Checking for Base64 encoding of header: " , myheaders
    if len(headersvalue) > 5:
        #check3 = isBase64(headersvalue)
        #check4 = isHex(headersvalue)
        check2 = isEncoded(headersvalue)

print ("\n\n")

print Style.RESET_ALL

if responsecode == "200":
    textcolor = Fore.GREEN
elif responsecode == "400" or responsecode == "401" or responsecode == "402" or responsecode == "403" or responsecode == "405" or responsecode == "444":
    textcolor = Fore.YELLOW
elif responsecode == "404":
    textcolor = Fore.WHITE
elif responsecode == "500" or responsecode == "501" or responsecode == "502" or responsecode == "503":
    textcolor = Fore.RED
elif responsecode == "414":
    textcolor = Fore.BLUE
else:
    textcolor = Fore.WHITE

print(textcolor + "Original Request Infos...")
print("==============================================================")
print("Original URL: " + url)
print("Final Landing Page: " + response.url)
print("Server: " + server)
print("Total Content-Length: " + responsecontentlen)
print("Response Code: " + responsecode)
print("Total Cookies: " + total_cookies)
print("Total Headers: " + total_headers) +  Style.RESET_ALL

print "\n\n"

####################################################################################################
print("Payload:   webcode / length / cookies / headers / server ")
print("==============================================================")

payloads = ['trace.axd','/admin/','/temp/','/tmp/','/bin/','?id=0','/api/','%','%%','&','<script>alert(1)</script>','%00','index.html','index.htm','index.php','index.jsp','index.asp','.git','.htaccess','.htpasswd','server-status','xmlrpc.php','sitemap.xml','login.php','%'*10050]


for pl in payloads:
    #dont append trailing slash - response = requests.get(url + "/", verify=False, headers=headers)
    try:
        response = requests.get(url + pl, verify=False, headers=headers)
        responsecode = str(response.status_code)
        responsecontent = (response.content)
        responseheaders = (response.headers)
        responsecookies = (response.cookies)
        responsecontentlen = str(len(response.content))
        responseheaderslen = str(len(response.headers))
        responsecookieslen = str(len(response.cookies))
        if responsecode == "200":
            textcolor = Fore.GREEN
        elif responsecode == "400" or responsecode == "401" or responsecode == "402" or responsecode == "403" or responsecode == "405" or responsecode == "444":
            textcolor = Fore.YELLOW
        elif responsecode == "404":
            textcolor = Fore.WHITE
        elif responsecode == "500" or responsecode == "501" or responsecode == "502" or responsecode == "503":
            textcolor = Fore.RED
        elif responsecode == "414":
            textcolor = Fore.BLUE
        else:
            textcolor = Fore.WHITE
        try:
            server = responseheaders['Server']
        except:
            pass
            server = '--'
        if len(pl) > 100:
            pl = "FLOOD OVER 9K!"
        if pl == "":
            pl = "DEFAULT"
        if pl == "<script>alert(1)</script>":
            pl = "<script>"
        if len(pl) < 7:
            print(textcolor + pl + ":\t\t" + responsecode + " / " + responsecontentlen + " / " + responsecookieslen + " / " + responseheaderslen + " /  " + server + Style.RESET_ALL)
        else:
            print(textcolor + pl + ":\t" + responsecode + " / " + responsecontentlen + " / " + responsecookieslen + " / " + responseheaderslen + " /  " + server + Style.RESET_ALL)
    except:
        pass
        if len(pl) > 100:
            pl = "FLOOD OVER 9000!"
        print(pl + ": " + "-" + " / " + "-" + " / " + "-" + " / " + "-")

####################################################################################################

try:
    response_robots = requests.get(url + 'robots.txt', verify=False, headers=headers)
    print("\n")
    response_robots.status_code = str(response_robots.status_code)
except:
    pass
    print("Unknown robots.txt request error!")

try:
    if response_robots.status_code == '200':
        print("Found robots.txt! ")
        print("==============================================================")
        robots = response_robots.content
        #robots = response_robots.decode()
        print (robots)
    else:
        print ("No robots.txt found. ")
        print("==============================================================")
except:
    pass
    print ("Error processing robots.txt.")

print"\n"


####################################################################################################
print "Testing HTTP Verb Responses..."
print "=============================================================="
verbs = ['OPTIONS', 'GET', 'POST', 'PUT', 'PATCH', 'HEAD', 'DELETE', 'CONNECT', 'TEST', 'TRACK', 'TRACE']


for verb in verbs:
    try:
        r = requests.request(verb, url, verify=False, headers=headers)
        responsecode1 = str(r.status_code)
        if responsecode1 == "200":
            textcolor = Fore.GREEN
        elif responsecode1 == "400" or responsecode1 == "401" or responsecode1 == "402" or responsecode1 == "403" or responsecode1 == "405" or responsecode1 == "444":
            textcolor = Fore.YELLOW
        elif responsecode1 == "404":
            textcolor = Fore.WHITE
        elif responsecode1 == "500" or responsecode1 == "501" or responsecode1 == "502" or responsecode1 == "503":
            textcolor = Fore.RED
        elif responsecode1 == "414":
            textcolor = Fore.BLUE
        else:
            textcolor = Fore.WHITE
        #print(textcolor)
        print textcolor + verb, r.status_code, r.reason + Style.RESET_ALL
    except:
        pass
        print verb, "ruhroh!"


print"\n"

####################################################################################################
print "Testing 'Host' header manipulation..."
print "=============================================================="
allhosts = [hosts, 'localhost', '127.0.0.1', '127.0.1.1', 'null', 'test', '0', '-1', 'admin', 'root']


for newhost in allhosts:
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
        'Host': newhost
    }
    ##### fuzz the host header
    try:
        response1 = session.get(url, verify=False, headers=headers, timeout=5)
        all_cookies = session.cookies.get_dict()
        all_headers = response1.headers
        responsecode = response1.status_code
        responsecode = str(responsecode)
        if responsecode == "200":
            textcolor = Fore.GREEN
        elif responsecode == "400" or responsecode == "403":
            textcolor = Fore.YELLOW
        elif responsecode == "404":
            textcolor = Fore.WHITE
        elif responsecode == "500" or responsecode == "503":
            textcolor = Fore.RED
        elif responsecode == "414":
            textcolor = Fore.BLUE
        else:
            textcolor = Fore.WHITE
        try:
            server = all_headers['Server']
        except:
            pass
            server = '--'
        try:
            responsecontentlen = str(len(response1.content))
            total_cookies = str(len(all_cookies))
            total_headers = str(len(all_headers))
        except:
            pass
            responsecontentlen = "-"
            total_cookies = "-"
            total_headers = "-"
            responsecode = ""
            response1.reason = ""
        if len(newhost) < 9:
            print (textcolor + newhost + ":\t\t\t" + responsecode + " / " + responsecontentlen + " / " +  response1.reason + "  /  " + server + Style.RESET_ALL)
        else:
            print (textcolor + newhost + ":\t\t" + responsecode + " / " + responsecontentlen + " / " +  response1.reason + "  /  " + server + Style.RESET_ALL)
    except:
        pass
        print (newhost + " : " + " MAJOR MALFUNCTION - SKIPPING ")

'''
###################### remove comments below to mirror the target site. ##########################################
print("\n\nNow performing WGET and saving files locally (Loading...please be patient.... ")
print("===============================================================================\n\n")
try:
    wget_command = "wget -m " + url + " 2>&1 | grep '^--' | awk '{ print $3 }' | grep -v '\.\(css\|js\|png\|gif\|jpg\|JPG\)$' > " + hosts + "--URLS.txt"
    os.system(wget_command)
except:
    pass
'''

print (Fore.GREEN + Style.BRIGHT + "\n====================  WisQuas (v0.7) Complete!  =====================\n\n")

sys.exit()

