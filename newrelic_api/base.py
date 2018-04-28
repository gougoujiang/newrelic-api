import os
import json
import base64
import requests

from .exceptions import ConfigurationException, NewRelicAPIServerException


class Resource(object):
    """
    A base class for API resources
    """
    URL = 'https://api.newrelic.com/v2/'
    URL_INSIGHTS_QUERY = 'https://insights-api.newrelic.com/v1/accounts/%s/query?nrql=%s'

    def __init__(self, api_key=None, query_account=None, query_key=None):
        """
        :type api_key: str
        :param api_key: The API key. If no key is passed, the environment
            variable NEW_RELIC_API_KEY is used.
        :raises: If the api_key parameter is not present, and no environment
            variable is present, a :class:`newrelic_api.exceptions.ConfigurationException`
            is raised.
        """
        self.api_key = api_key or os.environ.get('NEW_RELIC_API_KEY') or os.environ.get('NEWRELIC_API_KEY')
        
        # for insights query api
        self.query_account = query_account or os.environ.get('NEW_RELIC_QUERY_ACCOUNT') or os.environ.get('NEWRELIC_QUERY_ACCOUNT')
        self.query_key = query_key or os.environ.get('NEW_RELIC_QUERY_ACCOUNT') or os.environ.get('NEWRELIC_QUERY_ACCOUNT')

        if not self.api_key and not self.query_key:
            raise ConfigurationException('NEW_RELIC_API_KEY or NEWRELIC_API_KEY or NEW_RELIC_QUERY_KEY or NEWRELIC_QUERY_KEY not present in environment!')

        self.headers = {
            'Content-type': 'application/json'
        }
        
        if self.api_key:
            self.headers['X-Api-Key'] = self.api_key
        
        if self.query_key:
            self.headers['X-Query-Key'] = self.query_key

    def _get(self, *args, **kwargs):
        """
        A wrapper for getting things

        :returns: The response of your get
        :rtype: dict

        :raises: This will raise a
            :class:`NewRelicAPIServerException<newrelic_api.exceptions.NewRelicAPIServerException>`
            if there is an error from New Relic
        """
        response = requests.get(*args, **kwargs)
        if not response.ok:
            raise NewRelicAPIServerException('{}: {}'.format(response.status_code, response.text))

        json_response = response.json()

        if response.links:
            json_response['pages'] = response.links

        return json_response

    def _put(self, *args, **kwargs):
        """
        A wrapper for putting things. It will also json encode your 'data' parameter

        :returns: The response of your put
        :rtype: dict

        :raises: This will raise a
            :class:`NewRelicAPIServerException<newrelic_api.exceptions.NewRelicAPIServerException>`
            if there is an error from New Relic
        """
        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'])
        response = requests.put(*args, **kwargs)
        if not response.ok:
            raise NewRelicAPIServerException('{}: {}'.format(response.status_code, response.text))
        return response.json()

    def _post(self, *args, **kwargs):
        """
        A wrapper for posting things. It will also json encode your 'data' parameter

        :returns: The response of your post
        :rtype: dict

        :raises: This will raise a
            :class:`NewRelicAPIServerException<newrelic_api.exceptions.NewRelicAPIServerException>`
            if there is an error from New Relic
        """
        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'])
        response = requests.post(*args, **kwargs)
        if not response.ok:
            raise NewRelicAPIServerException('{}: {}'.format(response.status_code, response.text))
        return response.json()

    def _delete(self, *args, **kwargs):
        """
        A wrapper for deleting things

        :returns: The response of your delete
        :rtype: dict

        :raises: This will raise a
            :class:`NewRelicAPIServerException<newrelic_api.exceptions.NewRelicAPIServerException>`
            if there is an error from New Relic
        """
        response = requests.delete(*args, **kwargs)
        if not response.ok:
            raise NewRelicAPIServerException('{}: {}'.format(response.status_code, response.text))
        return response.json()

    def build_param_string(self, params):
        """
        This is a simple helper method to build a parameter string. It joins
        all list elements that evaluate to True with an ampersand, '&'

        .. code-block:: python

            >>> parameters = Resource().build_param_string(['filter[name]=dev', None, 'page=1'])
            >>> print parameters
            filter[name]=dev&page=1

        :type params: list
        :param params: The parameters to build a string with

        :rtype: str
        :return: The compiled parameter string
        """
        return '&'.join([p for p in params if p])
