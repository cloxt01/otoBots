import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class GraphQLClient:
    def __init__(self):
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1)
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Android 4.4; Mobile; rv:70.0) Gecko/70.0 Firefox/70.0',
            'X-Source': 'tokopedia-lite',
            'X-Device': 'lite-0.0',
            'X-Version': 'e96d138'
        }

    def post(self, operation, variables):
        payload = {
            'operationName': operation,
            'variables': variables,
            'query': self._get_query(operation)
        }
        response = self.session.post(
            'https://gql.tokopedia.com/graphql/' + operation,
            json=payload,
            headers=self.headers
        )
        return response.json()

    def _get_query(self, operation):
        queries = {
            'PDPGetDataP2': 'query PDPGetDataP2($productID: String!) {...}',
            'AddToCartOCCMulti': 'mutation AddToCartOCCMulti($items: [CartItemInput]!) {...}'
        }
        return queries.get(operation, '')