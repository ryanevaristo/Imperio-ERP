$(function(){
    $("#busca-produto").on("keyup", function(){
        let termo = $(this).val();
        if(termo.length > 2){
            $.get(buscarProdutosUrl, {q: termo}, function(data){
                $("#sugestoes").empty();
                data.forEach(function(prod){
                    $("#sugestoes").append(
                        `<a href="#" class="list-group-item list-group-item-action" 
                            data-id="${prod.id}" 
                            data-nome="${prod.nome}" 
                            data-qtd="${prod.qtd}">
                            ${prod.nome} (Estoque: ${prod.qtd})
                        </a>`
                    );
                });
            });
        } else {
            $("#sugestoes").empty();
        }
    });

    $("#sugestoes, .list-group").on("click", "a", function(e){
        e.preventDefault();
        let id = $(this).data("id");
        let nome = $(this).data("nome");
        let qtd = $(this).data("qtd");

        // Verificar se o produto já está no carrinho
        if ($(`#carrinho-body tr[data-id="${id}"]`).length > 0) {
            alert("Este produto já foi adicionado ao carrinho.");
            return;
        }

        $("#carrinho-body").append(`
            <tr data-id="${id}">
                <td>${nome}<input type="hidden" name="produtos" value="${id}"></td>
                <td>${qtd}</td>
                <td><input type="number" name="quantidade_${id}" min="0" class="form-control form-control-sm"></td>
                <td><button type="button" class="btn btn-danger btn-sm remover">Remover</button></td>
            </tr>
        `);

        $("#sugestoes").empty();
        $("#busca-produto").val("");
    });

    $("#carrinho-body").on("click", ".remover", function(){
        $(this).closest("tr").remove();
    });
});
