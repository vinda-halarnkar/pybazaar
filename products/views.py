from django.http import HttpResponse
# Create your views here.


def get_products(request):
    return HttpResponse("This is the products page")