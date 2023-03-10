from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from . import views
from authentication import views as a
from dashboard import views as d
from udashboard import views as u
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.DefaultView),
    # Auth
    path('registration', a.RegistrationView, name = 'reg'),
    path('login', a.LoginView, name = 'login'),
    path('logout', a.LogoutView, name = 'logout'),
    path('validate-username', csrf_exempt( a.UsernameValidationView), name='validate-username'),
    path('validate-email', csrf_exempt(a.EmailValidationView), name='validate-email'),
    path('activate/<uidb64>/<token>', a.VerificationView, name='activate'),
    path('request-reset-link', a.RequestPasswordResetEmail, name='reset'),
    path('set-new-password/<uidb64>/<token>', a.CompletePasswordReset, name='reset-user-password'),
    # Dashboard
    path('dashboard', d.DashboardView, name='dashboard'),
    path('application', d.ApplicationView, name='application'),
    path('markscardupload', d.MarksCardUploadView, name='markscardupload'),
    path('profile', d.ProfileView, name='profile'),
    path('reportcardupload', d.ReportCardUploadView, name='reportcardupload'),
    path('collegerecommender', d.CollegeRecommenderView, name='collegerecommender'),
    path('collegepredictor', d.CollegePredictorView, name='collegepredictor'),
    path('chart', d.chartView, name='chart'),
    # uDashboard
    path('dashboard', u.UDashboardView, name='udashboard'),
    path('profile', u.UProfileView, name='uprofile'),
    path('student-applications', u.UStudentsApplicationsView, name='sapplications'),
    path('uchangepassword', u.UChangePasswordView, name='uchangepassword'),
    path('viewstudentdata', u.UStudentDataView, name='viewstudentdata'),
    path('verifystudent', u.VerifyStudentView, name='verifystudent')]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)