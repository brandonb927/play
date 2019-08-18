from django.http import HttpResponse
from apps.utils.decorators import superuser_required


@superuser_required
def home(request):
    return HttpResponse("staff stuff here?")
