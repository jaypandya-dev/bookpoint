from django.http import HttpRequest,HttpResponse
from django.shortcuts import redirect, render

# Create your views here.
def home(request: HttpRequest):
    if request.COOKIES.get('email') is None:
        return redirect('/user/login')
    
    return render(request, 'core/home.html')