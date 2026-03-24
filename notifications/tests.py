import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from core.models import Empresa, NotificacoesGeral
from estoque.models import Produtos, Notificacao as NotificacaoEstoque
from notifications.models import Notification


@pytest.mark.django_db
class TestNotificationSignals:

    def test_create_notification_from_geral(self):
        empresa = Empresa.objects.create(nome="Empresa X")
        geral = NotificacoesGeral.objects.create(
            empresa=empresa,
            mensagem="Mensagem geral",
            visualizado=False
        )
        # Deve existir uma Notification correspondente
        ct = ContentType.objects.get_for_model(NotificacoesGeral)
        notif = Notification.objects.get(content_type=ct, object_id=geral.pk)
        assert notif.mensagem == "Mensagem geral"
        assert notif.empresa == empresa
        assert notif.visualizado is False

    def test_create_notification_from_estoque(self):
        empresa = Empresa.objects.create(nome="Empresa Y")
        produto = Produtos.objects.create(produto="Produto Teste")
        estoque = NotificacaoEstoque.objects.create(
            empresa=empresa,
            produto=produto,
            mensagem="Estoque baixo",
            visualizado=False
        )
        ct = ContentType.objects.get_for_model(NotificacaoEstoque)
        notif = Notification.objects.get(content_type=ct, object_id=estoque.pk)
        assert notif.mensagem == "Estoque baixo"
        assert notif.empresa == empresa
        assert notif.visualizado is False


@pytest.mark.django_db
class TestNotificationBackfill:

    def test_backfill_creates_notifications_once(self):
        empresa = Empresa.objects.create(nome="Empresa Z")
        geral = NotificacoesGeral.objects.create(empresa=empresa, mensagem="Teste", visualizado=False)
        produto = Produtos.objects.create(produto="Produto Backfill")
        estoque = NotificacaoEstoque.objects.create(empresa=empresa, produto=produto, mensagem="Teste estoque")

        # Simula backfill manual
        from django.core.management import call_command
        call_command("backfill_notifications")

        # Deve existir apenas uma Notification para cada origem
        ct_geral = ContentType.objects.get_for_model(NotificacoesGeral)
        ct_estoque = ContentType.objects.get_for_model(NotificacaoEstoque)
        assert Notification.objects.filter(content_type=ct_geral, object_id=geral.pk).count() == 1
        assert Notification.objects.filter(content_type=ct_estoque, object_id=estoque.pk).count() == 1


@pytest.mark.django_db
class TestNotificationAPI:

    def setup_method(self):
        self.client = APIClient()
        self.empresa = Empresa.objects.create(nome="Empresa API")
        # Simula usuário com empresa
        self.user = type("User", (), {"is_authenticated": True, "empresa": self.empresa})()
        self.client.force_authenticate(user=self.user)

    def test_list_notifications(self):
        geral = NotificacoesGeral.objects.create(empresa=self.empresa, mensagem="API geral")
        produto = Produtos.objects.create(produto="Produto API")
        NotificacaoEstoque.objects.create(empresa=self.empresa, produto=produto, mensagem="API estoque")

        url = reverse("notifications-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["results"]) == 2
        assert any("API geral" in n["mensagem"] for n in data["results"])

    def test_mark_notification_as_read(self):
        geral = NotificacoesGeral.objects.create(empresa=self.empresa, mensagem="API geral")
        notif = Notification.objects.first()
        url = reverse("notifications-mark-read", args=[notif.pk])
        response = self.client.patch(url)
        assert response.status_code == status.HTTP_200_OK
        notif.refresh_from_db()
        assert notif.visualizado is True