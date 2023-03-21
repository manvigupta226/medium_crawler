from django.urls import include

urlpatterns = [
    # ...
    path('myapp/', include('myapp.urls')),
    # ...
]
