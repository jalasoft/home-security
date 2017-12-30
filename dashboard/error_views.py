from django.shortcuts import render 

def error404(request):
    data = {}
    print("SRACKAAAAA|")
    return render(request, "dashboard/custom404.html", data)
    
    
def error500(request):
    data = {}
    return render(request, "dashboard/custom500.html", data);
