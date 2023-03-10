from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from dashboard . models import UserData
from django.contrib import messages
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/auth/login')
def UDashboardView(request):
    if request.method == 'GET':
        return render(request, 'udashboard/udashboard.html')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/auth/login')
def UProfileView(request):
    if request.method == 'GET':
        username = request.user.username
        email = request.user.email
        return render(request, 'udashboard/uprofile.html', {'username': username, 'email': email})
    else:
        return render(request, 'udashboard/uprofile.html')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/auth/login')
def UChangePasswordView(request):
    if request.method == 'POST':
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if pass1 != pass2:
            messages.error(request, 'The passwords don\'t match!')
            return redirect('profile')
        user = User.objects.get(username=request.user.username)
        user.set_password(pass1)
        user.save()
        messages.success(
            request, 'Password changed successfully! Please login again for security reasons!')
        return redirect('login')
    else:
        return redirect('uprofile')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/auth/login')
def UStudentsApplicationsView(request):
    if request.method == 'GET':
        if request.user.email == 'a@c.edu':
            data = UserData.objects.filter(submitted = True, Cambridge_verified = False)
        if request.user.email == 'a@h.edu':
            data = UserData.objects.filter(submitted = True, Harward_verified = False)
        if request.user.email == 'a@m.edu':
            data = UserData.objects.filter(submitted = True, MIT_verified = False)
        if request.user.email == 'a@o.edu':
            data = UserData.objects.filter(submitted = True, Oxford_verified = False)
        if request.user.email == 'a@s.edu':
            data = UserData.objects.filter(submitted = True, Stanford_verified = False)
        if request.user.email == 'a@u.edu':
            data = UserData.objects.filter(submitted = True, UCLA_verified = False)
        name = []
        course = []
        for d in data:
            if d.first_name:
                name.append(d.first_name)   
                course.append(d.course)
        return render(request, 'udashboard/sapplications.html', {'name':name, 'course':course , 'data':data})
    if request.method == 'POST':
        if request.user.email == 'a@c.edu':
            data = UserData.objects.filter(submitted = True, Cambridge_verified = False)
        if request.user.email == 'a@h.edu':
            data = UserData.objects.filter(submitted = True, Harward_verified = False)
        if request.user.email == 'a@m.edu':
            data = UserData.objects.filter(submitted = True, MIT_verified = False)
        if request.user.email == 'a@o.edu':
            data = UserData.objects.filter(submitted = True, Oxford_verified = False)
        if request.user.email == 'a@s.edu':
            data = UserData.objects.filter(submitted = True, Stanford_verified = False)
        if request.user.email == 'a@u.edu':
            data = UserData.objects.filter(submitted = True, UCLA_verified = False)
        name = []
        course = []
        for d in data:
            if d.first_name:
                if request.user.username in d.universities_applied:
                    name.append(d.first_name)
                    course.append(d.course)
        return render(request, 'udashboard/sapplications.html', {'name':name, 'course':course, 'data':data})
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/auth/login')
def UStudentDataView(request):
    if request.method == 'GET':
        return redirect('sapplications')
    if request.method == 'POST':
        student = UserData.objects.get(first_name=request.POST['name'])
        return render (request, 'udashboard/ViewStudent.html',{'student':student})
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/auth/login')
def VerifyStudentView(request):
    if request.method == 'GET':
        return redirect('sapplications')
    if request.method == 'POST':
        student = UserData.objects.get(first_name=request.POST['name'])
        if request.user.email == 'a@c.edu':
            student.Cambridge_verified = True
        if request.user.email == 'a@h.edu':
            student.Harward_verified = True
        if request.user.email == 'a@m.edu':
            student.MIT_verified = True
        if request.user.email == 'a@o.edu':
            student.Oxford_verified = True
        if request.user.email == 'a@s.edu':
            student.Stanford_verified = True
        if request.user.email == 'a@u.edu':
            student.UCLA_verified = True
        student.save()
        messages.success(request, 'Student '+student.first_name+' was verified successfully!')
        return redirect('sapplications')