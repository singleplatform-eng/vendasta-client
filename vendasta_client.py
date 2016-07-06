import requests

class VendastaEndpoint(object):

    def __init__(self, key, user, base_url):
        self.key = key
        self.user = user
        self.base_url = base_url

    def _call_vendasta(self, url, additional_params=None):
        params = {'apiKey': self.key, 'apiUser': self.user}
        if additional_params:
            params.update(additional_params)
        response = requests.post(url, params=params)
        return response.json()


class VendastaAccountsEndpoint(VendastaEndpoint):

    def create(self, data):
        """
        Creates a Vendasta account

        Returns a dict decoded from the JSON response returned
        by Vendasta

        Arguments:
            data -- a dict of the data to create the account
                    as described in the Vendasta documentation
        """
        url = self.base_url + '/v2/account/create/'
        return self._call_vendasta(url, data)

    def delete(self, data):
        """
        Deletes a Vendasta account

        Returns a dict decoded from the JSON response returned
        by Vendasta

        Arguments:
            data -- a dict of the data to delete the account
                    as described in the Vendasta documentation
        """
        url = self.base_url + '/v2/account/delete/'
        return self._call_vendasta(url, data)

    def search(self, data):
        """
        Search for a Vendasta account

        Returns a dict decoded from the JSON response returned
        by Vendasta

        Arguments:
            data -- a dict of the search terms to find the account
                    as described in the Vendasta documentation
        """
        url = self.base_url + '/v2/account/search/'
        return self._call_vendasta(url, data)


class VendastaReviewsEndpoint(VendastaEndpoint):

    def search(self, customer_id):
        """
        Gets all reviews for a Vendasta account

        Returns a dict decoded from the JSON response returned
        by Vendasta

        Arguments:
            customer_id -- The Vendasta customerIdentifier

        """
        url = self.base_url + '/v3/review/search/'
        params = {
            'customerIdentifier': customer_id,
            'pageSize': 500,
        }

        def get_all_results(previous_result):
            """
            Inner method for recursing through nextUrl until there
            are no more results

            Returns the full set of reviews that will be the return for
            'search(...)'

            Arguments:
                previous_result -- The modified result of previous calls
                                   to this endpoint
            """
            if not previous_result.get('nextUrl'):
                return previous_result
            else:
                result = self._call_vendasta(previous_result.get('nextUrl'))
                # Include the new list of reviews with the previous list
                previous_result['data'].extend(result['data'])
                result['data'] = previous_result['data']
                # Continue the recursion
                return get_all_results(result)

        # Make the initial call to Vendasta
        result = self._call_vendasta(url, params)

        # The number of reviews might exceed the page size so we check
        # for more reviews and retrieve them if so
        return get_all_results(result)


class Vendasta(object):

    endpoints = {
        'accounts': VendastaAccountsEndpoint,
        'reviews': VendastaReviewsEndpoint,
    }

    def __init__(self, key=None, user=None, base_url='https://reputation-intelligence-sandbox.vendasta.com/api'):
        self.key = key
        self.user = user
        self.base_url = base_url

    def __getattr__(self, name):
        endpoint = self.endpoints.get(name)
        return endpoint(self.key, self.user, self.base_url)
