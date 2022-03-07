from django.http import HttpResponse, JsonResponse
from .serializers import CourseSerializer
from course.models import Course



def courses(request):
    serializer = CourseSerializer(Course.objects.all(), many=True)
    return JsonResponse({'data':serializer.data})