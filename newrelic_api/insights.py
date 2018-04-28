from .base import Resource
import urllib

from .exceptions import NewRelicAPIServerException

class Insights(Resource):
    
    def __init__(self, query_account, query_key):
        Resource.__init__(self, None, query_account, query_key)
    
    def query(self, nrql = None):
        if not nrql: 
            raise NewRelicAPIServerException('Query statement is emtpy')
        
        return self._get(
            url=self.URL_INSIGHTS_QUERY % (self.query_account, urllib.quote(nrql)),
            headers=self.headers
        )
        