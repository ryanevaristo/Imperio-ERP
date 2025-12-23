from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()


class MensalidadeBackend(ModelBackend):
    """
    Backend de autenticação customizado que verifica o status da mensalidade
    da empresa antes de permitir o login.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Primeiro, autentica o usuário normalmente
        user = super().authenticate(request, username=username, password=password, **kwargs)
        
        if user is None:
            return None
        
        # Verifica se o usuário tem uma empresa associada
        if not hasattr(user, 'empresa') or user.empresa is None:
            # Se não tem empresa, permite o login (pode ser superuser)
            return user
        
        # Verifica o status da mensalidade da empresa
        empresa = user.empresa
        
        # Se a mensalidade não está ativa, bloqueia o acesso
        if not empresa.mensalidade_ativa:
            return None
        
        # Se tem data de vencimento e está vencida, bloqueia o acesso
        if empresa.data_vencimento_mensalidade:
            if date.today() > empresa.data_vencimento_mensalidade:
                return None
        
        # Se passou por todas as verificações, permite o login
        return user
    
    def user_can_authenticate(self, user):
        """
        Verifica se o usuário pode se autenticar, incluindo verificação de mensalidade.
        """
        is_active = super().user_can_authenticate(user)
        
        if not is_active:
            return False
        
        # Verifica mensalidade se o usuário tem empresa
        if hasattr(user, 'empresa') and user.empresa:
            return user.empresa.pode_acessar_sistema()
        
        return True
