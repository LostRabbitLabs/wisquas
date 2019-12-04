# wisquas
WisQuas (Reveal) - version: 0.6

=============================================================================

Inspiration...
http://wiki.ultimacodex.com/wiki/Reveal

"Wis Quas strips illusion from creatures hidden by the cloak of invisibility, instantly revealing their position. Nightshade cut many times to form a paper-like sheet, then carved into lace is secured by spider silk. It is glazed, dried in the sun, then crystallized into a shiny powder that must be tossed in the sky over the field of battle as the spell is cast."

---

Usage... Provide desired profile (desktop or mobile) along with URL and you are good to go.

// Show Help

./wisquas.py -h // HELP!!

// Use 'Desktop Browser' profile

./wisquas.py -1 "https://www.domain.com/directory/moreurl/"

// Use 'Mobile Browser' profile

./wisquas.py -2 "https://www.domain.com/directory/moreurl/"

// Use 'Custom Host Header' for requests



BONUS: ./wisquas.py -1 "https://www.domain.com/directory/moreurl/" custom_host_header_value

---

COMPLETED!
1. Merge 'ip' and 'dns' scripts into one master script
2. Add auto base64 decoding of cookies, headers (and more?)
3. Integrate openssl data points and output
4. Create Parameter for 'host:' header value

TO-DO
1. Add server and header stats to VERB enumeration function
2. Add custom host header to all requests
3. Add 'URLDecoder' for cookies/headers
4. Add double b64-decoding
5. Refactor all the holes.

