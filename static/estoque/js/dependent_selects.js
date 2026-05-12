document.addEventListener('DOMContentLoaded', function () {
    const empreendimentoSelect = document.querySelector('.empreendimento-select');
    const quadraSelect = document.querySelector('.quadra-select');
    const loteSelect = document.querySelector('.lote-select');

    if (!empreendimentoSelect || !quadraSelect || !loteSelect) {
        console.warn("Algum dos selects não foi encontrado no DOM.");
        return;
    }

    function preencherSelect(select, itens, placeholder, valueKey, textKey) {
        select.innerHTML = `<option value="">${placeholder}</option>`;
        itens.forEach(item => {
            const option = document.createElement('option');
            option.value = item[valueKey];
            option.textContent = item[textKey];
            select.appendChild(option);
        });
    }

    async function carregarQuadras(empreendimentoId) {
        if (!empreendimentoId) {
            preencherSelect(quadraSelect, [], 'Selecione a quadra', 'id', 'nome');
            preencherSelect(loteSelect, [], 'Selecione o lote', 'id', 'numero');
            return;
        }

        quadraSelect.innerHTML = '<option>Carregando...</option>';
        loteSelect.innerHTML = '<option value="">Selecione o lote</option>';

        try {
            const response = await fetch(`/estoque/get_quadras/${empreendimentoId}/`);
            const data = await response.json();
            preencherSelect(quadraSelect, data.quadras, 'Selecione a quadra', 'id', 'nome');
        } catch (error) {
            console.error('Erro ao carregar quadras:', error);
            quadraSelect.innerHTML = '<option value="">Erro ao carregar</option>';
        }
    }

    async function carregarLotes(quadraId) {
        if (!quadraId) {
            preencherSelect(loteSelect, [], 'Selecione o lote', 'id', 'numero');
            return;
        }

        loteSelect.innerHTML = '<option>Carregando...</option>';

        try {
            const response = await fetch(`/estoque/get_lotes/${quadraId}/`);
            const data = await response.json();
            preencherSelect(loteSelect, data.lotes, 'Selecione o lote', 'id', 'numero');
        } catch (error) {
            console.error('Erro ao carregar lotes:', error);
            loteSelect.innerHTML = '<option value="">Erro ao carregar</option>';
        }
    }

    empreendimentoSelect.addEventListener('change', function () {
        carregarQuadras(this.value);
    });

    quadraSelect.addEventListener('change', function () {
        carregarLotes(this.value);
    });

    // Inicialização automática (edição)
    if (empreendimentoSelect.value) {
        carregarQuadras(empreendimentoSelect.value).then(() => {
            if (quadraSelect.value) {
                carregarLotes(quadraSelect.value);
            }
        });
    }
});

