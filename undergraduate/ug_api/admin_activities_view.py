from rest_framework.views import APIView
from rest_framework.decorators import  api_view
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions,authentication
from rest_framework import status, generics
from django.db.models import Prefetch
from django.db.models import Q
import io, csv, pandas as pd
from django.db import  transaction
from base.baseHelper import session_semester_config, session_semester_config_always
from .ug_serializer import (SettingSerializer,LecturerCourseSerializer,RegistrationStudSerializer,UndergraduateProgrammeSerializer,ClassBroadsheetSemesterSessionSerializer,
                    UndergraduateProgrammeSerializer,UndergraduateCourseSerializer)
from undergraduate.models import (Faculty, Department,Programme,Course,Curriculum,
Registration,RegSummary,LecturerCourse)

from rest_framework.permissions import IsAuthenticated



class UndergraduateProgrammeList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UndergraduateProgrammeSerializer
    # http_method_names = ["get"]
    # pagination_class = PagePagination
    # filter_backends = (NullsAlwaysLastOrderingFilter, DjangoFilterBackend)
    # ordering_fields = ["created_date", "study"]
    # ordering = ["-created_date"]
