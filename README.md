# PigeonVision

# How to use

Enter a thing, we determine what that thing is, do our checks and give you a result. It couldn't be simpler!

# How it works

PigeonVision is a tool built by [Tom Blue](blog.tom-blue.co) and [Max Friedrich](m4x.uk) to determine how malicious various artefacts are.

We query various services such as virustotal, spamhaus and other threat intelligence sources, as well as checking DNS records, email configuration and location. We use this data to compute a score and determine a chance that the artefact is malicious.

The scores are inexact but you can scroll down and see in laymans terms the data we collected and how it was used.

Our aim is to appeal to everyone from your non technical grandma, to a technical SOC analyst. We provide a clear statement and use colours to illustrate how malicious we think something is, as well as providing the technical detail behind it.

# Estimative language

When dealing with uncertainties, estimative language is often used to convey the chances of something incurring.

This approach was [pioneered by the CIA](https://www.cia.gov/resources/csi/static/Words-of-Estimative-Probability.pdf), and although their specific language doesn't fit our needs here (we wouldn't want to say something is "Probably not" malicious if there's a 40% chance), we've adapted it to our use.

Our confidence intervals and language used in our statements are as follows:

- 100%: Certain
- Between 87% and 99%: Almost certain
- Between 60% and 86%: Probable
- Between 40% and 59%: About even
- Between 20% and 39%: Realistic but low possibility
- Between 1% and 19%: Unlikely
- 0%: Certainly not (only in the case of presence on whitelist e.g. google.com)

# Methodology

We have a number of heuristics we use, some of them are purely informative like geolocation - they don't contribute to the score but the information is available to the user. The heuristics that do contribute to the score all get weighted, each one will return a certainty between 0 and 1. 

We add up all the certainties multiplied by their weights and do a weighted mean to get an average score - so for example if heuristic A has a weight of 20% and returns 0.5 and heuristic B has a weight of 100% and returns 1, we do (0.5 \* 0.2 + 1 \* 1) / (1 + 0.2) = (0.1 + 1) / (1.2) = 1.1/1.2 = 0.9167 or a final score of 91.67%.

The scores heuristics return depend on the individual heuristic. Some sources such as hybrid analysis already compute a score out of 100, in those cases we just take that. 

In other cases we either have some data which we try to interpret where we can and display anyways where we can, and quite often this involves a bit of curve fitting. 

As an example, a problem with virus total is that if 1 or 2 out of 90 engines detect something, it's probably not malicious, but if 10 or 12 detect something, it's maybe something new. If 10 out of 90 engines detect something we want a score much greater than 11.1%, but if 1 or 2 detect it we don't want to give it significant weight, so we fit it onto a curve where a few engines detecting something doesn't result in a very high score, but if a considerable number do, then it does.

# Heuristics used

- https://check.spamhaus.org 
- https://www.hybrid-analysis.com/ 
- https://threatfox.abuse.ch/ 
- virus total 
- whois 
- geolocation 
- safebrowsing 
- dns lookup 
- SPF 
- DMARC 

# Future Heuristics

This is a list of things we intend to add but have not yet got around to.

- https://otx.alienvault.com/ 
- blacklist checker 
- Team Cymru 5
- Censys 
