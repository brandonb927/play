# Adds the account object to the request if the user is authenticated
class AccountDecoratorMiddlware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.account = request.user.account
        else:
            request.account = None

        response = self.get_response(request)

        return response
