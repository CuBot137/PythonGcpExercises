import functions_framework
from flask import request, jsonify # Handle HTTP request and create JSON response

@functions_framework.http
def http_handler(request):
    method = request.method

    if method == 'GET':
        return handle_get(request)
    elif method == 'POST':
        return handle_post(request)
    elif method == 'DELETE':
        return handle_delete(request)
    else:
        return ('Unknown method', 405)



def handle_get(request):
    response = {
        'message': 'This is a GET response',
        'status': 'Success'
    }
    return jsonify(response), 200

def handle_post(request):
    response = {
        'message':'This is a POST response',
        'status':'Success'
    }
    return jsonify(response), 200

def handle_delete(request):
    response = {
        'message':'This is a DELETE response',
        'status':'Success'
    }
    return jsonify(response), 200

