from django.shortcuts import render

# Create your views here.
## Accueil
def accueil(request):
    return render(request, 'general/index.html', {})