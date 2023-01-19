from django.http import HttpResponse


def package(request):
    return HttpResponse({'data':'No record!'})