# PigeonVision

# Estimative language

When dealing with uncertainties, estimative language is often used to convey the chances of something incurring.

This approach was [pioneered by the CIA](https://www.cia.gov/resources/csi/static/Words-of-Estimative-Probability.pdf), and although their specific language doesn't fit our needs here (we wouldn't want to say something is "Probably not" malicious if there's a 40% chance), we've adapted it to our use.

Our confidence intervals and language used in our statements are as follows:

- 100%: Certain
- Between 87% and 99%: Almost certain
- Between 60% and 86%: Probable
- Between 40% and 59%: About even
- Between 20% and 39%: Realistic possibility
- Between 1% and 19%: Unlikely
- 0%: Certainly not (only in the case of presence on whitelist e.g. google.com)

# Heuristics used

- https://check.spamhaus.org 80% 
- https://otx.alienvault.com/ 50%
- virus total 95%
- https://threatfox.abuse.ch/ 80%
- whois 100%
- geolocation 70%
- safebrowsing 90%
- blacklist checker 80%
- dns lookup 100%
- Team Cymru 50%
- SPF 100%
- DMARC 100%
- Censys 90%
- https://www.hybrid-analysis.com/ 90%
