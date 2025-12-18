from .models import Empresa

def empresa_context(request):
    """
    Adiciona informações da empresa do usuário logado ao contexto dos templates
    """
    if request.user.is_authenticated and hasattr(request.user, 'empresa') and request.user.empresa:
        return {
            'empresa_atual': request.user.empresa,
            'empresa_nome': request.user.empresa.nome,
        }
    return {}
