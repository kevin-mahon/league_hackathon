

def get_error_string(code):
    match code:
        case 400:
            return "Bad Request - The request was invalid or cannot be otherwise served."
        case 401:
            return "Unauthorized - No valid API key provided."
        case 403:
            return "Forbidden - The API key doesn't have permissions to perform the request."
        case 404:
            return "Not Found - The requested resource could not be found."
        case 405:
            return "Method Not Allowed - The request method is not supported for the specified resource."
        case 415:
            return "Unsupported Media Type - The request entity has a media type which the server or resource does not support."
        case 429:
            return "Too Many Requests - Rate limit exceeded."
        case 500:
            return "Internal Server Error - We had a problem with our server. Try again later."
        case 502:
            return "Bad Gateway - The server was acting as a gateway or proxy and received an invalid response from the upstream server."
        case 503:
            return "Service Unavailable - The server is currently unavailable (because it is overloaded or down for maintenance)."
        case 504:
            return "Gateway Timeout - The server was acting as a gateway or proxy and did not receive a timely response from the upstream server."
        case _:
            return None
