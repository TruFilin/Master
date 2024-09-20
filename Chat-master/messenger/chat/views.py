import json
from django.http import JsonResponse
from .models import GroupChat, Message
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .models import CustomUser  # Импортируй CustomUser
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import GroupChat
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.views import View
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
User = get_user_model()
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()  # Используйте вашу модель пользователя
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class RegisterPageView(View):
    def get(self, request):
        return render(request, 'chat/register.html')

class GroupChatListCreateView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)  # Получаем данные как JSON
        chat_name = data.get('name')

        if not chat_name:
            return JsonResponse({'error': 'Chat name is required.'}, status=400)

        chat = GroupChat.objects.create(name=chat_name)
        return JsonResponse({'id': chat.id, 'name': chat.name})

class GroupChatPageView(View):
    def get(self, request):
        chats = GroupChat.objects.all()  # Получаем все групповые чаты
        return render(request, 'chat/group_chats.html', {'chats': chats})  # Передаем чаты в контекст

class GroupChatDetailView(LoginRequiredMixin, View):
    def get(self, request, chat_id):
        chat = get_object_or_404(GroupChat, id=chat_id)

        # Добавляем пользователя в чат, если его там нет
        if request.user not in chat.members.all():
            chat.members.add(request.user)

        return render(request, 'chat/chat_detail.html', {'chat': chat})  # Передаем чат в контекст




class DeleteGroupChatView(LoginRequiredMixin, View):
    def post(self, request, chat_id):
        chat = get_object_or_404(GroupChat, id=chat_id)
        chat.delete()
        return JsonResponse({'message': 'Чат успешно удален.'})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)  # Используем request.FILES для обработки загрузки файлов
        if form.is_valid():
            form.save()
            return redirect('group_chat_page')  # Перенаправление после сохранения
    else:
        form = UserProfileForm(instance=request.user)  # Заполнение формы текущими данными пользователя
    return render(request, 'chat/edit_profile.html', {'form': form})


class LoginView(auth_views.LoginView):
    def get_success_url(self):
        messages.success(self.request, "Вы успешно вошли в систему.")
        return super().get_success_url()

class UserListView(View):
    def get(self, request):
        users = User.objects.all()  # Получаем всех пользователей
        return render(request, 'chat/user_list.html', {'users': users})  # Передаем всех пользователей в контекст

class UserChatDetailView(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        # Логика для отображения чата с пользователем
        # Например, можно создать/получить групповой чат для общения
        return render(request, 'chat/chat_detail.html', {'user': user})


class SendMessageView(LoginRequiredMixin, View):
    def post(self, request, chat_id):
        chat = get_object_or_404(GroupChat, id=chat_id)
        data = json.loads(request.body)
        content = data.get('content')

        if not content:
            return JsonResponse({'error': 'Content is required.'}, status=400)

        try:
            message = Message.objects.create(chat=chat, user=request.user, content=content)
            return JsonResponse({'user': message.user.username, 'content': message.content})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



def csrf_failure(request, reason=""):
    return render(request, 'chat/csrf_failure.html', {'reason': reason})