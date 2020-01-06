# wisquas.py
Inspiration... http://wiki.ultimacodex.com/wiki/Reveal

"Wis Quas strips illusion from creatures hidden by the cloak of invisibility, instantly revealing their position. Nightshade cut many times to form a paper-like sheet, then carved into lace is secured by spider silk. It is glazed, dried in the sun, then crystallized into a shiny powder that must be tossed in the sky over the field of battle as the spell is cast."

     Language: Python 2
     Libraries: tldextract, urlparse, sys, requests, socket, pprint, os, urllib3, colorama, base64, binascii, codecs, ssl, json
     Purpose: Penetration Testing / URL Revealer


Provide a URL to WisQuas and it will perform the following functions...
1. Resolve hostname to IP address
2. Perform ASN lookup on IP address to provide ownership info and possible geolocation
3. Inventories all received headers and cookies and attempts to auto-decode their values (hex/b64)
4. Baseline original URL request (with SSL cert info if HTTPS) to compare to all other requests
5. Tactical fuzzing and enumeration to generate unique errors and reveal layered web services
6. Inspect robots.txt file if available
7. Enumerate through possible HTTP Verbs
8. Perform Host Header Manipulation to detect additional accessible containers


# Install
Follow the steps below to install 'wisquas'.

     git clone https://github.com/lostrabbitlabs/wisquas
     cd wisquas
     chmod 755 wisquas.py
     pip install tldextract --upgrade


# Usage
Provide desired browsing profile (desktop or mobile) along with URL (with trailing backslash as needed!).


     // Show Help
     ./wisquas.py -h

     // Use 'Desktop Browser' profile
     ./wisquas.py -1 "https://www.domain.com/"

     // Use 'Mobile Browser' profile
     ./wisquas.py -2 "https://www.domain.com/directory/moredirs/"


# Output
When completed will create colorized console output!


# Bonus

     // Use 'Custom Host Header' for requests
     ./wisquas.py -1 "https://www.domain.com/directory/moreurl/" custom_host_header_value

     // Use WGET to mirror site and create file of all discovered URLS
     ---uncomment the code within
     
     // Use IP ADDRESS instead of hostname
     ./wisquas.py -1 "https://192.168.0.1/"


