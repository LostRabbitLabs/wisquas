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

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

cookie_lib = []

def helpme():
    print ('\nWisQuas (Reveal) - Example usage:\n')
    print ("Using 'Desktop Browser' profile...")
    print ("./wisquas-v1.py -1 'https://www.domain.com/dir1/dir2/otherstuff/'\n")
    print ("Using 'Mobile Browser' profile...")
    print ("./wisquas-v1.py -2 'https://www.domain.com/dir1/dir2/otherstuff/'")
    sys.exit()

try:
    url = sys.argv[2]
except:
    helpme()


if url[-1:] != "/":
    url = url + "/"

agent = sys.argv[1]

if agent not in ["-1","-2"]:
    helpme()


print (Fore.GREEN + Style.BRIGHT + "\n")
print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
print("-    Wis Quas (dns) - Level 6 - REVEAL  -")
print("-    http://github.com/LostRabbitLabs   -")
print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n")

if agent == "-1":
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }
    print "Using 'Desktop Browser' profile for crawling..."
    print "=============================================================="  + Style.RESET_ALL
else:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid Build/FRG22D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
    }
    print "Using 'Mobile Browser' profile for crawling..."
    print "=============================================================="  + Style.RESET_ALL


o = urlparse(url)
host = tldextract.extract(o.netloc)
hostname = tldextract.extract(o.netloc)
domainname = host.domain + "." + host.suffix
hostname2 = hostname.subdomain + "." + domainname
hosts = str(hostname2)
proto = o.scheme

if hosts[0] == ".":
    hosts = hosts[1:]

if hosts == 'localhost.':
    hosts = 'localhost'

host_ip = socket.gethostbyname(hosts)

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

print "\n"

print "Total Headers: " + total_headers
print "=============================================================="
for myheaders in all_headers:
    headersvalue = all_headers[myheaders]
    output2 = myheaders + " :: " + headersvalue
    print output2

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

payloads = ['%','%%','&','<script>alert(1)</script>','%00','index.html','index.htm','index.php','index.jsp','index.asp','.git','.htaccess','server-status','xmlrpc.php','sitemap.xml','login.php','%'*10050]


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
verbs = ['OPTIONS', 'GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'CONNECT', 'TEST', 'TRACE']


for verb in verbs:
    try:
        r = requests.request(verb, url)
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

print (Fore.GREEN + Style.BRIGHT + "\n=====================  WisQuas (dns) Complete!  =====================\n\n")

sys.exit()



