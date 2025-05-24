import requests

from pigeonvision.heuristics.base.result import Result
from pigeonvision.heuristics.base import Heuristic
from pigeonvision.validate import QueryType

class spamhaus(Heuristic):

	def fetch(query: str, query_type: QueryType) -> Result:

		res = requests.get('https://check.spamhaus.org/api/checker/query/', data={'query': query})

		print(res)