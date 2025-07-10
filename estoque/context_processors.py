from .models import Notificacao


def notificacoes_context(request):
    if request.user.is_authenticated:
        notificacoes = Notificacao.objects.filter(visualizado=False).order_by('-data_criacao')[:10]
        return {
            'notificacoes': notificacoes,
            'notificacoes_count': notificacoes.count()
        }
    return {
        'notificacoes': [],
        'notificacoes_count': 0
    }
