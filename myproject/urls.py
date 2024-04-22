
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('myapp.urls')),  # Include URL patterns from your app
    path('admin/', admin.site.urls),

]
