# Chad Fusco
import json
from typing import Any
from urllib.request import Request, urlopen


class Client:
    """Use this Client class to send information and check for a valid response."""
    FAILED_REQUEST = object()  # Look below to see how this sentinel is used.

    @classmethod
    def send_json(cls, method, url, python_obj=None) -> Any:
        """Converts the python_obj parameter into a JSON string and sends that JSON to the server. Returns server's response converted back from JSON to a Python object."""
        if python_obj is not None:
            json_string = json.dumps(python_obj)
            json_bytes = json_string.encode('utf-8')
        else:
            json_bytes = b''
        request = Request(
            url=url,
            method=method,
            headers={
                'Content-Length': len(json_bytes),
                'Content-Type': 'application/json',
            },
            data=json_bytes
        )
        response = urlopen(request)
        if 200 <= response.status <= 299:
            # Any status in the 200 range is considered a successful response.
            response_data_bytes = response.read()
            response_data_string = response_data_bytes.decode('utf-8')
            reconstituted_python_object = json.loads(response_data_string)
            request_result = reconstituted_python_object
        else:
            request_result = cls.FAILED_REQUEST
        return request_result


def print_result(result):
    if result is Client.FAILED_REQUEST:
        print(f"REQUEST FAILED for {sample_data_to_send=}")
    else:
        print(f"REQUEST SUCCEEDED:")
        print(result)


if __name__ == '__main__':
    """
    THIS IS HOW YOU TEST YOUR MICROSERVICE
    """

    # TODO: Set your base server url according to how you are running your server.
    base_server_url = "http://localhost:8080"
    intended_path = "/"
    full_server_url = base_server_url + intended_path

    # TODO: Create the data you want to send.
    sample_data_to_send = {'func': '+', 'args': [1, 2, 3]}  # Any combination of JSON-compatible Python objects: int, float, str, list, dict, True/False/None

    print_result(Client.send_json('GET', full_server_url, sample_data_to_send))

    # TEST MATH_OLD
    intended_path = '/math_old'
    full_server_url = base_server_url + intended_path
    print_result(Client.send_json('POST', full_server_url, sample_data_to_send))

    # TEST POST NUMS
    intended_path = '/nums'
    sample_data_to_send = [1, 2, 3]
    full_server_url = base_server_url + intended_path
    print_result(Client.send_json('POST', full_server_url, sample_data_to_send))

    # TEST GET NUMS
    print_result(Client.send_json('GET', full_server_url)) # should return [1, 2, 3]

    # TEST PUT NUMS
    sample_data_to_send = [4, 5]
    print_result(Client.send_json('PUT', full_server_url, sample_data_to_send))

    # TEST GET NUMS
    print_result(Client.send_json('GET', full_server_url)) # should return [1, 2, 3, 4, 5]

    # TEST GET NUMS/SUM
    intended_path = '/nums/sum'
    full_server_url = base_server_url + intended_path
    print_result(Client.send_json('GET', full_server_url)) # should return 15

    # TEST POST NUMS - ERROR CASE
    intended_path = '/nums'
    sample_data_to_send = 'hello'
    full_server_url = base_server_url + intended_path
    print_result(Client.send_json('POST', full_server_url, sample_data_to_send))

    # TEST PUT NUMS
    sample_data_to_send = ['wrong', 'type']
    print_result(Client.send_json('PUT', full_server_url, sample_data_to_send))
