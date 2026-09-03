from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse

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
        subject_field = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        if name and email and message:
            if subject_field:
                subject = f'[AIDN Contact] {subject_field} - Message de {name}'
                body = f"Nom : {name}\nEmail : {email}\nObjet : {subject_field}\n\nMessage :\n{message}"
            else:
                subject = f'[AIDN Contact] Message de {name}'
                body = f"Nom : {name}\nEmail : {email}\n\nMessage :\n{message}"
            try:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Votre message a été envoyé avec succès !')
            except Exception:
                messages.error(request, "Une erreur est survenue lors de l'envoi. Veuillez réessayer.")
        else:
            messages.error(request, 'Veuillez remplir tous les champs.')

    return redirect(request.META.get('HTTP_REFERER', 'accueil'))

## Contact Produits
def contact_email_products(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject_field = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        if not (name and email and subject_field and message):
            return JsonResponse({'status': 'error', 'message': 'Veuillez remplir tous les champs.'})

        subject = f'Proposition de Marché : {subject_field}'
        body = f"Nom : {name}\nEmail : {email}\nObjet : {subject_field}\n\nMessage :\n{message}"
        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            return JsonResponse({'status': 'success', 'message': 'Votre message a été envoyé avec succès !'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': "Une erreur est survenue lors de l'envoi. Veuillez réessayer."})

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)