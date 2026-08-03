"""
Context processor pour rendre l'organisation courante disponible dans tous les templates.
"""


def organization(request):
    """Retourne l'organisation résolue par le middleware."""
    return {
        'organization': getattr(request, 'organization', None),
    }
