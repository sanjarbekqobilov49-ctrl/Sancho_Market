from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role != 'admin':
            messages.error(request, 'Siz admin emassiz!')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
