from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import Product, Sale
from django.db import transaction
from undergraduate.models import Registration
from base.baseHelper import session_semester_config



from django.utils import timezone

def my_view(request):
    now = timezone.now()
    formatted_date = now.strftime('%Y-%m-%d')
    formatted_time = now.strftime('%H:%M:%S')
    return HttpResponse(f'Current date: {formatted_date}, current time: {formatted_time}')


def test_score_input(request):
    i_course_code = request.POST.get('course','')
    if i_course_code is not None:
        reg = Registration.objects.filter(course_code= i_course_code, semester = session_semester_config.semester_code, session_id_fk=session_semester_config.session)
        return render(request, 'base/test_score_input.html',context={'data':reg})
    return JsonResponse({'Error':"Course Code is required"})




def test_bulk_create_view(request):

    # return JsonResponse({'status':'Success'}, safe=False)
    in_data = [
        {'name':'rice 100','quantity':'10','week':'1','price':'200'},
        {'name':'rice 100','quantity':'10','week':'2','price':'300'},
        {'name':'beans 200','quantity':'5','week':'1','price':'1000'},
        {'name':'Gari 300','quantity':'5','week':'2','price':'1000'},
      
    ]
    # with transaction.atomic():
        # for index, row in enumerate(in_data, start=1):
        #     # create = Product.objects.create(name=row['name'], quantity=row['quantity'], week=row['week'], price=row['price'])
        #     # update = Product.objects.filter(id=index).update(name=row['name'])
        #     bulk_pro = []
        #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        #     print(update)
        #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    bulk_pro = [Product(name=row['name'], quantity=row['quantity'], week=row['week'], price=row['price']) for row in in_data]
    bulk_create = Product.objects.bulk_create(bulk_pro, ignore_conflicts=True)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    for stud in bulk_create:
        print(stud.name)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    return render(request, 'base/test_signal.html',context={'data':in_data})





user_ids_dict = {
  1: 100,
  2: 150,
  3: 500
  # this dict can contain n key value pairs.
}



# from django.db import transaction

# with transaction.atomic():
#   for key, value in user_ids_dict:
#     # User.objects.filter(id=key).update(score=value)
#     pass


