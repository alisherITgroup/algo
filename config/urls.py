from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    path('', include('home.urls')),
    path('problemsets/', include('problemsets.urls')),
    path('problems/', include('problems.urls')),
    path('contests/', include('contests.urls')),
    path('chats/', include('chat.urls')),
    path('quizzes/', include('quizzes.urls')),
    path('attempts/', include('attempts.urls')),
    path('posts/', include('posts.urls')),
    path('courses/', include('courses.urls')),
    path('projects/', include('projects.urls')),
    path('api/v1/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)