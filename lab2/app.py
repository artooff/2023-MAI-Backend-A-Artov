def app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    response_body = b'Hello, World!\n'
    start_response(status, headers)
    return [response_body]