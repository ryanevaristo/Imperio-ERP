document.addEventListener('DOMContentLoaded', function() {
    const empreendimentoSelects = document.querySelectorAll('.empreendimento-select');

    empreendimentoSelects.forEach(empreendimentoSelect => {
        const modal = empreendimentoSelect.closest('.modal');
        const quadraSelect = modal.querySelector('.quadra-select');
        const loteSelect = modal.querySelector('.lote-select');

        if (!quadraSelect || !loteSelect) return;

        // Função para atualizar quadras
        function updateQuadras(empreendimentoId) {
            if (!empreendimentoId) {
                quadraSelect.innerHTML = '<option value="">---------</option>';
                loteSelect.innerHTML = '<option value="">---------</option>';
                return;
            }

            fetch(`/estoque/get_quadras/${empreendimentoId}/`)
                .then(response => response.json())
                .then(data => {
                    quadraSelect.innerHTML = '<option value="">---------</option>';
                    data.quadras.forEach(quadra => {
                        const option = document.createElement('option');
                        option.value = quadra.id;
                        option.textContent = quadra.nome;
                        quadraSelect.appendChild(option);
                    });
                    // Limpar lotes
                    loteSelect.innerHTML = '<option value="">---------</option>';
                })
                .catch(error => console.error('Erro ao carregar quadras:', error));
        }

        // Função para atualizar lotes
        function updateLotes(quadraId) {
            if (!quadraId) {
                loteSelect.innerHTML = '<option value="">---------</option>';
                return;
            }

            fetch(`/estoque/get_lotes/${quadraId}/`)
                .then(response => response.json())
                .then(data => {
                    loteSelect.innerHTML = '<option value="">---------</option>';
                    data.lotes.forEach(lote => {
                        const option = document.createElement('option');
                        option.value = lote.id;
                        option.textContent = lote.numero;
                        loteSelect.appendChild(option);
                    });
                })
                .catch(error => console.error('Erro ao carregar lotes:', error));
        }

        // Event listeners
        empreendimentoSelect.addEventListener('change', function() {
            updateQuadras(this.value);
        });

        quadraSelect.addEventListener('change', function() {
            updateLotes(this.value);
        });

        // Inicializar se já houver valor selecionado (para edição)
        if (empreendimentoSelect.value) {
            updateQuadras(empreendimentoSelect.value);
            // Se quadra também estiver selecionada, atualizar lotes
            setTimeout(() => {
                if (quadraSelect.value) {
                    updateLotes(quadraSelect.value);
                }
            }, 100); // Pequeno delay para garantir que quadras sejam carregadas
        }
    });
});
