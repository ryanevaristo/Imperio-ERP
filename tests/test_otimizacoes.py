"""
Testes para validar as otimizações implementadas no Imperio ERP
Execute com: python manage.py test tests.test_otimizacoes
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.db import connection
from django.test.utils import override_settings
from django.core.cache import cache

from core.models import Empresa
from cliente.models import Cliente
from estoque.models import Produtos, EstoqueCategoria
from financeiro.models import ContaPagar, ContaReceber, DespesasCategoria
from produto.models import Empreendimento, Quadra, Lote

import time

User = get_user_model()


class ConnectionPoolingTestCase(TestCase):
    """Testa se o connection pooling está configurado corretamente"""
    
    def test_conn_max_age_configured(self):
        """Verifica se CONN_MAX_AGE está configurado"""
        conn_max_age = connection.settings_dict.get('CONN_MAX_AGE')
        self.assertIsNotNone(conn_max_age, "CONN_MAX_AGE não está configurado")
        self.assertEqual(conn_max_age, 600, "CONN_MAX_AGE deve ser 600 segundos")
    
    def test_connection_timeout_configured(self):
        """Verifica se o timeout de conexão está configurado"""
        options = connection.settings_dict.get('OPTIONS', {})
        self.assertIn('connect_timeout', options, "connect_timeout não está configurado")
        self.assertEqual(options['connect_timeout'], 10, "connect_timeout deve ser 10 segundos")


class CacheTestCase(TestCase):
    """Testa se o sistema de cache está funcionando"""
    
    def setUp(self):
        cache.clear()
    
    def test_cache_set_and_get(self):
        """Testa se o cache consegue armazenar e recuperar valores"""
        cache.set('test_key', 'test_value', 60)
        value = cache.get('test_key')
        self.assertEqual(value, 'test_value', "Cache não está funcionando corretamente")
    
    def test_cache_expiration(self):
        """Testa se o cache expira corretamente"""
        cache.set('test_key_expire', 'test_value', 1)
        time.sleep(2)
        value = cache.get('test_key_expire')
        self.assertIsNone(value, "Cache não está expirando corretamente")


class QueryOptimizationTestCase(TestCase):
    """Testa se as queries estão otimizadas"""
    
    def setUp(self):
        # Criar empresa de teste
        self.empresa = Empresa.objects.create(
            nome="Empresa Teste",
            cnpj="12.345.678/0001-90"
        )
        
        # Criar usuário de teste
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            empresa=self.empresa,
            cargo='A'
        )
        
        # Criar dados de teste
        self.categoria_estoque = EstoqueCategoria.objects.create(
            nome_categoria="Categoria Teste",
            empresa=self.empresa
        )
        
        self.categoria_despesa = DespesasCategoria.objects.create(
            nome_categoria="Despesa Teste"
        )
        
        # Criar 10 produtos
        for i in range(10):
            Produtos.objects.create(
                produto=f"Produto {i}",
                qtd=100,
                qtd_min=10,
                custo=50.00,
                categoria=self.categoria_estoque,
                empresa=self.empresa
            )
        
        # Criar 10 clientes
        for i in range(10):
            Cliente.objects.create(
                nome_completo=f"Cliente {i}",
                cpf_cnpj=f"123.456.789-{i:02d}",
                email=f"cliente{i}@test.com",
                empresa=self.empresa
            )
    
    def test_cliente_list_queries(self):
        """Testa se a listagem de clientes usa select_related"""
        self.client.force_login(self.user)
        
        # Resetar queries
        connection.queries_log.clear()
        
        with self.assertNumQueries(3):  # Deve usar poucas queries com select_related
            response = self.client.get('/clientes/')
        
        self.assertEqual(response.status_code, 200)
    
    def test_estoque_list_queries(self):
        """Testa se a listagem de estoque usa select_related"""
        self.client.force_login(self.user)
        
        connection.queries_log.clear()
        
        with self.assertNumQueries(4):  # Deve usar poucas queries
            response = self.client.get('/estoque/')
        
        self.assertEqual(response.status_code, 200)


class ExportOptimizationTestCase(TestCase):
    """Testa se as exportações estão otimizadas"""
    
    def setUp(self):
        # Criar empresa de teste
        self.empresa = Empresa.objects.create(
            nome="Empresa Teste Export",
            cnpj="98.765.432/0001-10"
        )
        
        # Criar usuário de teste
        self.user = User.objects.create_user(
            username='exportuser',
            email='export@test.com',
            password='testpass123',
            empresa=self.empresa,
            cargo='A'
        )
        
        # Criar clientes para exportação
        for i in range(5):
            Cliente.objects.create(
                nome_completo=f"Cliente Export {i}",
                cpf_cnpj=f"987.654.321-{i:02d}",
                email=f"export{i}@test.com",
                empresa=self.empresa
            )
    
    def test_export_clientes_xlsx_queries(self):
        """Testa se a exportação de clientes usa poucas queries"""
        self.client.force_login(self.user)
        
        connection.queries_log.clear()
        
        # A exportação deve usar apenas 1-2 queries com select_related e only()
        with self.assertNumQueries(2, msg="Exportação deve usar no máximo 2 queries"):
            response = self.client.get('/clientes/exportar_xlsx/')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    def test_export_clientes_performance(self):
        """Testa se a exportação é rápida"""
        self.client.force_login(self.user)
        
        start_time = time.time()
        response = self.client.get('/clientes/exportar_xlsx/')
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(
            execution_time, 
            2.0, 
            f"Exportação demorou {execution_time:.2f}s, deve ser < 2s"
        )


class IndexTestCase(TestCase):
    """Testa se os índices foram criados corretamente"""
    
    def test_cliente_indexes_exist(self):
        """Verifica se os índices do modelo Cliente existem"""
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Obter nome da tabela
            table_name = Cliente._meta.db_table
            
            # Query para listar índices (PostgreSQL)
            cursor.execute(f"""
                SELECT indexname 
                FROM pg_indexes 
                WHERE tablename = '{table_name}'
            """)
            
            indexes = [row[0] for row in cursor.fetchall()]
            
            # Verificar se existem índices
            self.assertGreater(
                len(indexes), 
                1, 
                "Deve haver índices além da primary key"
            )
    
    def test_produtos_indexes_exist(self):
        """Verifica se os índices do modelo Produtos existem"""
        from django.db import connection
        
        with connection.cursor() as cursor:
            table_name = Produtos._meta.db_table
            
            cursor.execute(f"""
                SELECT indexname 
                FROM pg_indexes 
                WHERE tablename = '{table_name}'
            """)
            
            indexes = [row[0] for row in cursor.fetchall()]
            
            self.assertGreater(
                len(indexes), 
                1, 
                "Deve haver índices além da primary key"
            )


class PerformanceTestCase(TestCase):
    """Testes de performance geral"""
    
    def setUp(self):
        self.empresa = Empresa.objects.create(
            nome="Empresa Performance",
            cnpj="11.222.333/0001-44"
        )
        
        self.user = User.objects.create_user(
            username='perfuser',
            email='perf@test.com',
            password='testpass123',
            empresa=self.empresa,
            cargo='A'
        )
        
        # Criar dados em massa
        clientes = [
            Cliente(
                nome_completo=f"Cliente Perf {i}",
                cpf_cnpj=f"111.222.333-{i:02d}",
                email=f"perf{i}@test.com",
                empresa=self.empresa
            )
            for i in range(50)
        ]
        Cliente.objects.bulk_create(clientes)
    
    def test_list_page_performance(self):
        """Testa se a página de listagem carrega rapidamente"""
        self.client.force_login(self.user)
        
        start_time = time.time()
        response = self.client.get('/clientes/')
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(
            execution_time,
            1.0,
            f"Página de listagem demorou {execution_time:.2f}s, deve ser < 1s"
        )


# Executar testes
if __name__ == '__main__':
    import django
    django.setup()
    
    from django.test.runner import DiscoverRunner
    runner = DiscoverRunner(verbosity=2)
    runner.run_tests(['tests.test_otimizacoes'])
