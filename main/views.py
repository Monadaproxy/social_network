from django.shortcuts import render

def index_index(request):
    return render(request, 'main/index_index.html')

def about_about(request):
    return render(request, 'main/about_about.html')
