from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm
        
        
class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        # Call the parent class's form_valid() method to save the new user object
        response = super().form_valid(form)

        # Authenticate the user with the password they just provided
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)

        # Log the user in
        login(self.request, user)

        return response