# Chad Fusco
from flask import Flask, request, jsonify
app = Flask(__name__)

nums = []

@app.route('/', methods=['GET', 'POST'])
def index():
    """The base route returns the equivalent of a How-To page."""
    return {
        'sample_calls': [
            {
                'path': '/',
                'method': 'GET',
                'data': None,
                'result': 'Returns this information.',
            },
            # TODO: Replace the examples below with 6+ distinct sample calls to your API.
            {
                'path': '/nums',
                'method': 'POST',
                'data': [1, 2, 3],
                'result': 'success',
            },
            {
                'path': '/nums',
                'method': 'GET',
                'data': None,
                'result': [1, 2, 3],
            },
            {
                'path': '/nums',
                'method': 'PUT',
                'data': [4, 5],
                'result': 'success',
            },
            {
                'path': '/nums/sum',
                'method': 'GET',
                'data': None,
                'result': 15,
            },
            {
                'path': '/nums',
                'method': 'POST',
                'data': 'hello',
                'result': {'error': 'Failed request.'},
            },
            {
                'path': '/nums',
                'method': 'PUT',
                'data': ['wrong', 'type'],
                'result': {'error': 'Failed request.'},
            },
        ]
    }


# TODO: Replace the '/math' route and math_service() function with your microservice routes and functions.
@app.route('/math_old', methods=['POST'])
def math_service_old():
    request_data = request.json
    try:
        function = request_data['func']
        args = request_data['args']
        if function == '+':
            result = sum(args)
            result = {"sum": result}
        elif function == '*':
            result = 1
            for value in args:
                result *= value
            result = {"product": result}
        else:
            result = error_msg("Unrecognized function.")
    except Exception as err:
        print(err)
        print(f"{request_data=}")
        result = error_msg("Failed request.")
    return result


@app.get('/nums')
def get_nums():
    return nums


@app.post('/nums')
def post_nums():
    global nums
    data = request.json
    result = jsonify('success')
    try:
        check_is_num_list(data)
        nums = data
    except Exception as err:
        print(err)
        print(f"{data=}")
        result = error_msg("Failed request.")
    return result


@app.put('/nums')
def put_nums():
    global nums
    data = request.json
    result = jsonify('success')
    try:
        check_is_num_list(data)
        nums.extend(data)
    except Exception as err:
        print(err)
        print(f"{data=}")
        result = error_msg("Failed request.")
    return result


@app.get('/nums/sum')
def get_sum_nums():
    return jsonify(sum(nums))


def error_msg(msg: str) -> dict:
    """Wraps the error message in a JSON-friendly dict for clear communication."""
    return {"error": msg}


def check_is_num_list(my_list):
    if type(my_list) != list:
        raise TypeError
    for num in my_list:
        if type(num) != int and type(num) != float:
            raise TypeError


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
