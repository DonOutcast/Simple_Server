from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler


class Handlers(BaseHTTPRequestHandler):

    def _headers(self, content_type: tuple) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header(*content_type)
        self.end_headers()

    def _get_html(self, message: str) -> bytes:
        content = f"""
                                <html>
                                      <head>
                                            <meta charset='utf-8'>
                                            <title>
                                                    Простой HTTP-сервер
                                            </title>
                                      </head>
                                      <body>
                                            <h1>
                                                <p>
                                                    {message}
                                                </p>
                                            </h1>
                                      </body>
                                </html>
                            """

        return content.encode("utf8")

    def _not_found_html(self) -> bytes:
        content = f"""
                                        <html>
                                              <head>
                                                    <meta charset='utf-8'>
                                                    <title>
                                                            Простой HTTP-сервер
                                                    </title>
                                              </head>
                                              <body>
                                                    <h1>
                                                        404 Not Found!
                                                    </h1>
                                              </body>
                                        </html>
                                    """

        return content.encode("utf8")

    def _not_found(self):
        self.send_response(HTTPStatus.NOT_FOUND)
        self._headers(("Content-typ", "text/html"))
        self.wfile.write(self._not_found_html())

    def do_GET(self):
        if self.path == "/":
            self._headers(("Content-type", "text/html"))
            message = "Hello, World!"
            self.wfile.write(self._get_html(message))
        else:
            self._not_found()


def run_server(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    try:
        print("Server running...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
    finally:
        print("Server stop.")


if __name__ == "__main__":
    run_server(handler_class=Handlers)
