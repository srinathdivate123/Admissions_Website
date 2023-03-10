from django.shortcuts import redirect

def DefaultView(request):
    return redirect('login')