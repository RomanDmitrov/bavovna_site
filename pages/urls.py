from  django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('set-language/<str:lang_code>/', views.set_language, name='set_language'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('gdpr-data-request-policy/', views.gdpr_policy, name='gdpr_policy'),
]