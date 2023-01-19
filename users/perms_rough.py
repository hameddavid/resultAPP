from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist

# Example 1 start
user_login_required = user_passes_test(lambda user: user.is_active, login_url='/')

def active_user_required(view_func):
    decorated_view_func = login_required(user_login_required(view_func))
    return decorated_view_func

@active_user_required
def index(request):
    return render(request, 'index.html')

# Example 1 end

# Example 2 start 
# Not, this method is defined in the user model as property
def is_recruiter(self):   
    if str(self.user_type) == 'Recruiter':
        return True
    else:
        return False
# in the view
rec_login_required = user_passes_test(lambda u: True if u.is_recruiter else False, login_url='/')
# in the view
def recruiter_login_required(view_func):
    decorated_view_func = login_required(rec_login_required(view_func), login_url='/')
    return decorated_view_func

@recruiter_login_required
def index(request):
    return render(request, 'index.html')
# Example 2 end

# Example 3 start
# Not everything is defined inside the model class
class Meta:
    permissions = (
            ('blog_view', 'can view blog posts and categories'),
            ('blog_edit', 'can edit blog category and post'),
            ("support_view", "can view tickets"),
            ("support_edit", "can edit tickets"),
            ("activity_view", "can view recruiters, applicants, data, posts"),
            ("activity_edit", "can edit data"),
        )
def has_perm(self, perm, obj=None):
    try:
        user_perm = self.user_permissions.get(codename=perm)
    except ObjectDoesNotExist:
        user_perm = False
    if user_perm:
        return True
    else:
        return False
def permission_required(*perms):
    return user_passes_test(lambda u: any(u.has_perm(perm) for perm in perms), login_url='/')


@permission_required("activity_view", "activity_edit")
def index(request):
    return render(request, 'index.html')
# Example 3 end

