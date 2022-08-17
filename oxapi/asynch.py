from typing import List, Union

import oxapi
from oxapi.abstract.api import ModelAPI


class AsyncCallPipe:
    """Class for performing multiple calls to OxAPI in parallel."""

    def __init__(self, call_list: List[ModelAPI] = None):
        """Constructor.

        Args:
            call_list: the list of API calls. It is allowed to create an AsyncCallPipe without its call_list
            defined at instantiation time (calls can be added later with add method).
        """
        if call_list is None:
            call_list = []
        self.__call_list = call_list

    def run(self):
        """Runs the set of API calls.

        Returns:
            List : the List of API calls with their result (or errors).
        """
        import grequests

        if len(self.__call_list) == 0:
            oxapi.logger.warning("Call list is empty, nothing to run.")
            return
        reqs = []
        for call in self.__call_list:
            api_type: ModelAPI = call
            reqs.append(
                grequests.post(
                    api_type.get_url(),
                    json=api_type._body,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": oxapi.api_key,
                    },
                )
            )

        results = grequests.map(
            requests=reqs, exception_handler=AsyncCallPipe.__exception_handler
        )
        results_processed = []
        for i in range(0, len(results)):
            temp = self.__call_list[i]
            temp.parse_error_message(results[i], raise_exceptions=False)
            if results[i].status_code == 200:
                temp.result = results[i].json()
            results_processed.append(temp)
        return results_processed

    def add(self, api_call: Union[ModelAPI, List[ModelAPI]]):
        """Adds a single or a list of API calls to the call list.

        Args:
            api_call: single or list of API calls to be added.
        """
        if isinstance(api_call, List):
            self.__call_list = self.__call_list + api_call
        elif isinstance(api_call, ModelAPI):
            self.__call_list.append(api_call)

    def flush(self):
        """Clears the list of API calls."""
        self.__call_list = []

    @staticmethod
    def __exception_handler(request, exception):
        """Handles the exceptions in calling the APIs.

        Args:
            request: original request
            exception: generated exception
        """
        oxapi.logger.warning(
            "Request failed: {0}, ERROR: {1}".format(request.url, exception)
        )
