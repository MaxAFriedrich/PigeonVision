# TODO

- which queries ran and outcomes in a seperate log file
- add sha256 HA support
- [LevelBlue Labs](https://otx.alienvault.com/)
- [Blacklist Checker](https://blacklistchecker.com/)
- [Team Cymru 5](https://www.team-cymru.com/)
- [Censys](https://search.censys.io/)
- [Phishtank](https://phishtank.org/)
- [UrlHaus](https://urlhaus.abuse.ch/) (Improve heuristic certainty, hack in initial query)

# Complex TODO

- Malicious redirects

We only get maliciousness for final redirect

Let's say URL A redirects to B redirects to C, URL A is indexed by URLHaus, B drops malware so VT and C is benign

We say URL A is benign because the final URL (C) is, however malware was dropped at B and our own heuristic said A was malicious

We need to do get the maximum maliciousness from each heuristic at every stage 

e.g.

heur 	|URL A 	|URL B 	|URL C 	|Final
URLHAUS |0.6	|0	 	|0 		|0
SPAMHAUS|0		|0		|0.2 	|0
VT		|0		|0.5 	|0		|0

should result in URLHAUS(0.6), SPAMHAUS(0.2), VT(0.5)
currently results in 0 for each heuristic

- Other links

It would be a good idea to download the HTML of webpages we can, parse out other links and run checks on them too
