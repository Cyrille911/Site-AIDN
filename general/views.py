from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

# Create your views here.
## Accueil
def accueil(request):
    return render(request, 'general/accueil.html', {})

## Nos Produits
def nos_produits(request):
    return render(request, 'general/products.html', {})

## A propos
def a_propos(request):
    return render(request, 'general/a_propos.html', {})

## Portfolio
def portfolio(request):
    return render(request, 'general/portfolio.html', {})

## Nous joindre
def nous_joindre(request):
    return render(request, 'general/nous_joindre.html', {})

## Voir plus
def voir_plus(request):
    return render(request, 'general/voir_plus.html', {})

## Contact
def contact_email(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        if name and email and message:
            subject = f'[AIDN Contact] Message de {name}'
            body = f"Nom : {name}\nEmail : {email}\n\nMessage :\n{message}"
            try:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    ['aidn.tech@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, 'Votre message a été envoyé avec succès !')
            except Exception:
                messages.error(request, "Une erreur est survenue lors de l'envoi. Veuillez réessayer.")
        else:
            messages.error(request, 'Veuillez remplir tous les champs.')

    return redirect('accueil')