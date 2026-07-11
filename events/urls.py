from django.urls import path
from . import views


urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('gallery/', views.gallery, name='gallery'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('<int:pk>/comment/', views.comment_add, name='comment_add'),
    path('<int:pk>/comments/', views.event_comments, name='event_comments'),
    path('presigned-upload-url/', views.get_presigned_upload_url, name='presigned_upload_url'),
]