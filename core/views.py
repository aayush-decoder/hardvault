from django.shortcuts import render


def home(request):
    """Landing page"""
    return render(request, 'home.html')


def about(request):
    """About page"""
    return render(request, 'about.html')
