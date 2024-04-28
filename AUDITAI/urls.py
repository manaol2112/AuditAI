
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from appAUDITAI.dataview.ADMIN.views.systemsettings import ManageUsersandRolesView,verification_error_view, email_verification_view,verification_success_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('appAUDITAI.urls',namespace='appAUDITAI')),
    path('verify/<str:uidb64>/<str:token>/', email_verification_view, name='email_verification'),
    path('verification-success/<str:uidb64>/<str:token>/', verification_success_view, name='verification_success'), 
    path('verification-error/', verification_error_view, name='verification_error'), 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
