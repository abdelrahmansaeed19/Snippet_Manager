from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView, ListView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.db.models import Q

class HomePageView(TemplateView):
    template_name = 'blog/base.html'

class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'blog/login.html'
    def get_success_url(self):
        messages.success(self.request, "You have successfully logged in.")
        return reverse_lazy('home')
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return self.render_to_response(self.get_context_data(form=form))

class CustomLogoutView(LogoutView):
    pass

class ProfileDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/profile_detail.html'

class ProfileUpdateView(LoginRequiredMixin, FormView):
    template_name = 'blog/profile_edit.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('profile-detail')

    http_method_names = ['get', 'post']  # <-- contains "method"

    def post(self, request, *args, **kwargs):
        """Handle POST requests to update user profile details."""
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your profile has been updated.")
        return super().form_valid(form)
