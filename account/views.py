from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from reservation import models
from django.views.generic import CreateView
from django.conf import settings
from django.urls import reverse_lazy
from .forms import UserRegisterForm
from .models import UserProfile

class RoomListView(generic.ListView, LoginRequiredMixin):
    model = models.Room
    template_name = "reservation/index.html"

    def get_queryset(self):
        available_rooms = models.Room.objects.all()
        return available_rooms

class UserRegisterView(CreateView):
    model = settings.AUTH_USER_MODEL
    form_class = UserRegisterForm
    template_name = "account/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.set_password(form.cleaned_data["password"])
        self.object.save()
        # ユーザープロフィールを作成する
        UserProfile.objects.create(
            user=self.object, user_type=form.cleaned_data["user_type"]
        )
        return response