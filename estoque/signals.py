from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Produtos, Movimentacao


@receiver(post_save, sender=Movimentacao)
def atualizar_estoque(sender, instance, **kwargs):

    movimentacao = instance
    produto = movimentacao.produto

    if movimentacao.tipo == 'Entrada':
        produto.qtd += movimentacao.qtd
    elif movimentacao.tipo == 'Saída':
        produto.qtd -= movimentacao.qtd
    elif movimentacao.tipo == 'Devolução':
        produto.qtd += movimentacao.qtd
        
    produto.save()