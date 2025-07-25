from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/auth/login/')
def home(request):
    return render(request, 'home.html')

def error_403_view(request, exception):
    return render(request, '403.html', status=403)