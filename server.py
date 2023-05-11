from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """The base route returns the equivalent of a How-To page."""
    return {
        'sample_calls': [
            {
                'path': '/',
                'data': None,
                'result': 'Returns this information.',
            },
            # TODO: Replace the examples below with 6+ distinct sample calls to your API.
            {
                'path': '/math',
                'data': {'func': '+', 'args': [1, 2, 3, 4]},
                'result': {'sum': 10},
            },
            {
                'path': '/math',
                'data': {'func': '*', 'args': [1, 2, 3, 4]},
                'result': {'product': 24},
            },
        ]
    }


# TODO: Replace the '/math' route and math_service() function with your microservice routes and functions.
@app.route('/math', methods=['POST'])
def math_service():
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


def error_msg(msg: str) -> dict:
    """Wraps the error message in a JSON-friendly dict for clear communication."""
    return {"error": msg}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
