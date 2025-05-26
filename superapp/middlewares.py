from django.shortcuts import redirect


def check_login(get_response):
    def wrapper(request):
        if not request.user.is_authenticated:
            url = request.META["PATH_INFO"]

            return redirect(f"/login?url={url}")

        response = get_response(request)
        return response

    return wrapper
