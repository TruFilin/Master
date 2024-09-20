from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/chat/register/', permanent=False)),  # Перенаправление на страницу регистрации
    path('chat/', include('chat.urls')),  # Подключение URL приложения chat
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # URL для страницы входа
]
