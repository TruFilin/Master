from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    RegisterPageView,
    RegisterView,
    SendMessageView,
    GroupChatListCreateView,
    edit_profile,
    GroupChatDetailView,
    DeleteGroupChatView,
    UserListView,
    GroupChatPageView
)

urlpatterns = [
    path('register/', RegisterPageView.as_view(), name='register_page'),  # Для отображения HTML-страницы регистрации
    path('edit-profile/', edit_profile, name='edit_profile'),  # Маршрут для редактирования профиля
    path('api/register/', RegisterView.as_view(), name='register'),  # Для API регистрации
    path('group-chats/', GroupChatPageView.as_view(), name='group_chat_page'),  # Для отображения HTML-страницы групповых чатов
    path('api/group-chats/', GroupChatListCreateView.as_view(), name='group_chat_list_create'),  # Для создания групповых чатов
    path('api/group-chats/<int:chat_id>/send-message/', SendMessageView.as_view(), name='send_message'),  # Для отправки сообщений
    path('api/group-chats/<int:chat_id>/delete/', DeleteGroupChatView.as_view(), name='delete_group_chat'),  # Для удаления группового чата
    path('users/', UserListView.as_view(), name='user_list'),  # Маршрут для списка пользователей
    path('login/', auth_views.LoginView.as_view(), name='login'),  # URL для страницы входа
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # URL для выхода
    path('api/group-chats/<int:chat_id>/send-message/', SendMessageView.as_view(), name='send_message'),
    path('group-chats/<int:chat_id>/', GroupChatDetailView.as_view(), name='group_chat_detail'),  # Для отображения детальной информации о чате

]
