import csv
from rest_framework.decorators import  api_view
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from base.models import Setting


# @login_required(login_url='index')
@api_view(['GET', 'POST'])
def loadCSV(request):
    return Response({'data':"Done"})    
    with open("C:/Users/PC/Desktop/T_SESSION_DATA.csv") as f:
        data = csv.reader(f)

        for ind,row in enumerate(data) :
            if ind == 0:
                continue
            # row = Staff(**datum)
            # row.save()
            print(row[0])
            set = Setting(    
                session =row[0] ,
                semester_name = 'FIRST SEMESTER' if row[1] == 1 else 'SECOND SEMESTER' ,
                semester_code = row[1]
            )
            set.save()

    
    return Response({'data':"Done"})








# @login_required(login_url='index')
# @api_view(['GET', 'POST'])
# def loadJson(request):    
#     with open("C:/Users/PC/Desktop/New folder/data_export_13_12_2022/T_PROG_COURSE.json") as f:
#         records = json.load(f)

#     for record in records:   

#         fac = Curriculum( 
#            program = record['prog_code'],
#            course_code = record['course_code'],
#            status = record['status'],
#            last_updated_by_old = record['last_updated_by'],
#            last_updated_date_old = record['last_update_date'],
#            course_reg_level = record['course_level'],
#            semester = record['semester'],
#            register_flag = record['register_flag'],
           
#             last_updated_by_new=request.user,
         
#             )
#         fac.save()
#         # return Response({'data':record})
    
#     return Response({'data':records[0:4]})




# @login_required(login_url='index')
