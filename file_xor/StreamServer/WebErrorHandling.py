from quart import render_template, request


class HTTPError(Exception):
    status_code:int = None
    description:str = None
    def __init__(self, status_code, description):
        self.status_code = status_code
        self.description = description
        super().__init__(self.status_code, self.description)

error_messages = {
    400: 'Invalid request.',
    401: 'File code is required to download the file.',
    403: 'Invalid file code.',
    404: 'File not found.',
    500: 'Internal server error.'
}

async def invalid_request(_):
    message = error_messages.get(400)
    accept = request.headers.get('Accept', '')
    if 'text/html' in accept or '*/*' in accept:
        return await render_template('WebError.html', status=400, title=message, message=message), 400
    return message, 400

async def not_found(_):
    message = error_messages.get(404)
    accept = request.headers.get('Accept', '')
    if 'text/html' in accept or '*/*' in accept:
        return await render_template('WebError.html', status=404, title=message, message=message), 404
    return message, 404

async def invalid_method(_):
    message = 'Invalid request method.'
    accept = request.headers.get('Accept', '')
    if 'text/html' in accept or '*/*' in accept:
        return await render_template('WebError.html', status=405, title=message, message=message), 405
    return message, 405

async def http_error(error: HTTPError):
    error_message = error_messages.get(error.status_code)
    message = error.description or error_message

    # If the client accepts HTML, render a friendly error page.
    accept = request.headers.get('Accept', '')
    if 'text/html' in accept or '*/*' in accept:
        hints = {
            401: 'Provide the file code as the `code` query parameter.',
            403: 'Check that the provided file code is correct.',
            404: 'The requested file id does not exist.',
            416: 'Requested range not satisfiable for this resource.'
        }
        hint = hints.get(error.status_code)
        return await render_template('WebError.html', status=error.status_code, title=message, message=message, hint=hint), error.status_code

    return message, error.status_code

def abort(status_code: int = 500, description: str = None):
    raise HTTPError(status_code, description)