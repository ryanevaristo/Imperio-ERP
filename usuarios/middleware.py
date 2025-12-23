from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import auth, messages
from django.utils.deprecation import MiddlewareMixin


class MensalidadeMiddleware(MiddlewareMixin):
    """
    Middleware que verifica o status da mensalidade em cada requisição.
    Se a mensalidade vencer durante uma sessão ativa, desloga o usuário.
    """
    
    # URLs que não precisam de verificação de mensalidade
    EXEMPT_URLS = [
        '/auth/login/',
        '/auth/logout/',
        '/admin/',
        '/static/',
        '/media/',
    ]
    
    def process_request(self, request):
        # Verifica se a URL atual está na lista de exceções
        path = request.path
        for exempt_url in self.EXEMPT_URLS:
            if path.startswith(exempt_url):
                return None
        
        # Se o usuário não está autenticado, não faz nada
        if not request.user.is_authenticated:
            return None
        
        # Se o usuário não tem empresa, permite acesso (pode ser superuser)
        if not hasattr(request.user, 'empresa') or request.user.empresa is None:
            return None
        
        # Verifica o status da mensalidade
        empresa = request.user.empresa
        
        if not empresa.pode_acessar_sistema():
            # Mensalidade vencida - desloga o usuário
            auth.logout(request)
            messages.error(
                request,
                'Sua mensalidade venceu. Entre em contato com o suporte para renovar o acesso ao sistema.',
                extra_tags='danger'
            )
            return redirect(reverse('usuarios:login'))
        
        return None
