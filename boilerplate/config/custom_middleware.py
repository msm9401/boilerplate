import re
from time import process_time_ns

from rest_framework.status import is_client_error, is_success
from rest_framework import views


class ProcessTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        view_process_start_time = process_time_ns()
        response = self.get_response(request)
        view_process_end_time = process_time_ns()

        if not response.has_header("process_time"):
            response["View-Process-Run-Time"] = (
                view_process_end_time - view_process_start_time
            )

        return response


class ResponseFormatMiddleware:
    METHOD = ("GET", "POST", "PUT", "PATCH", "DELETE")

    def __init__(self, get_response):
        self.get_response = get_response
        self.API_URLS = [
            re.compile(r"^(.*)/api"),
            re.compile(r"^api"),
        ]

    def __call__(self, request):
        response = None
        if not response:
            response = self.get_response(request)
        if hasattr(self, "process_response"):
            response = self.process_response(request, response)
        return response

    def process_response(self, request, response):
        """
        API_URLS 와 method 가 확인이 되면
        response 로 들어온 data 형식에 맞추어
        response_format 에 넣어준 후 response 반환
        """
        path = request.path_info.lstrip("/")
        valid_urls = (url.match(path) for url in self.API_URLS)

        if request.method in self.METHOD and any(valid_urls):
            response_format = {
                "success": is_success(response.status_code),
                "result": {},
                "message": None,
            }

            if hasattr(response, "data") and getattr(response, "data") is not None:
                data = response.data

                try:
                    response_format["message"] = data.pop("message")
                except (KeyError, TypeError):
                    response_format.update({"result": data})
                finally:
                    if is_client_error(response.status_code):
                        response_format["result"] = None
                        response_format["message"] = data
                    else:
                        response_format["result"] = data

                    response.data = response_format
                    response.content = response.render().rendered_content

            else:
                response.data = response_format

        return response
