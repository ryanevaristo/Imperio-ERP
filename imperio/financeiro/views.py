from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import ContaPagar, ContaReceber, Cheque
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator


@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def contas_pagar(request):
    contas_pagar = ContaPagar.objects.all()
    template = loader.get_template('contas_pagar.html')
    context = {
        'contas_pagar': contas_pagar,
    }
    return HttpResponse(template.render(context, request))