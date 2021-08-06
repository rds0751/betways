from django.shortcuts import render

def error_404(request, exception):
    data = {}
    return render(request,'users/404.html', data)

def error_500(request):
    data = {}
    return render(request,'users/500.html', data)

def error_400(request, exception):
    data = {}
    return render(request,'users/404.html', data)

def error_403(request, exception):
    data = {}
    return render(request,'users/500.html', data)