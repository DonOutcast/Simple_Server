import json
import urllib
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
        # content = f"""
        #                                 <html>
        #                                       <head>
        #                                             <meta charset='utf-8'>
        #                                             <title>
        #                                                     Простой HTTP-сервер
        #                                             </title>
        #                                       </head>
        #                                       <body>
        #                                             <h1>
        #                                                 404 Not Found!
        #                                             </h1>
        #                                       </body>
        #                                       <script>
        #                                         console.log(1);
        #                                         let user = {
        #                                           name: 'John',
        #                                           surname: 'Smith'
        #                                         };
        #
        #                                         let response = await fetch('/article/fetch/post/user', {
        #                                           method: 'POST',
        #                                           headers: {
        #                                             'Content-Type': 'application/json;charset=utf-8'
        #                                           },
        #                                           body: JSON.stringify(user)
        #                                         });
        #
        #                                         let result = await response.json();
        #                                         alert(result.message);
        #                                       </script>
        #                                 </html>
        #                             """

        # return content.encode("utf8")
        with open("index.html", "rb") as f:
            return f.read()

    def _post_html(self):
        # content = f"""
        #                 <form action="/" method="POST">
        #           <div>
        #             <label for="say">What greeting do you want to say?</label>
        #             <input name="say" id="say" value="Hi" />
        #           </div>
        #           <div>
        #             <label for="to">Who do you want to say it to?</label>
        #             <input name="to" id="to" value="Mom" />
        #           </div>
        #           <div>
        #             <button>Send my greetings</button>
        #           </div>
        #         </form>
        # """
        # return content.encode("utf8")
        with open("post.html", "rb") as f:
            return f.read()

    def _not_found(self):
        self.send_response(HTTPStatus.NOT_FOUND)
        self._headers(("Content-typ", "text/html"))
        self.wfile.write(self._not_found_html())

    def _post_page(self):
        self._headers(("Content-type", "text/html"))
        self.wfile.write(self._post_html())

    def _process_post_urlencoded(self) -> dict[str, str]:
        length = int(self.headers["Content-Length"])
        data = self.rfile.read(length).decode("ascii")
        result = {}
        for pair in data.split("&"):
            key, value = pair.split("=", 1)
            result[urllib.parse.unquote(key)] = urllib.parse.unquote(value)
        return result

    def do_GET(self):
        if self.path == "/":
            self._headers(("Content-type", "text/html"))
            message = "Hello, World!"
            self.wfile.write(self._get_html(message))
        elif self.path == "/say":
            self._post_page()
        else:
            self._not_found()

    def dict_as_html_table(self, data: dict[str, str]) -> str:
        """ Форматирование словаря в виде HTML таблицы """
        lines = []
        for key, val in data.items():
            lines.append(f"<tr><td>{key}</td><td>{val}</td></tr>")

        return f"<table border=\"1\"><tr><th>key</th><th>value</th></tr>{''.join(lines)}</table>"

    def simple_page(self, body: str = "<h1>Subscribe to @FlongyDev</h1>"):
        """ Статическая страница с фиксированным HTML """
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=UTF-8")
        self.end_headers()

        self.wfile.write(body.encode("utf-8"))

    def do_POST(self):
        content_type = self.headers["Content-type"]
        print(content_type)
        if content_type == "application/json":
            # result = self._process_post_urlencoded()
            # self.simple_page(self.dict_as_html_table(result))
            self._headers(("Content-type", "application/json"))
            print("True".encode("utf8"))
            self.wfile.write(json.dumps({"POST": True}).encode("utf8"))
        # elif "application/json" in content_type:
        #     print("Hello World POST")
        #     # self.wfile.write(str({"POST": True}).encode("utf8"))
        #     length = int(self.headers["Content-Length"])
        #     message = json.loads(self.rfile.read(length))
        #
        #     # add a property to the object, just to mess with data
        #     message['received'] = 'ok'
        #
        #     # send the message back
        #     self._headers(("Content-type", "application/json"))
        #     print("True".encode("utf8"))
        #     self.wfile.write(json.dumps({"POST": True}).encode("utf8"))
        else:
            self.log_error("Unknown")


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
