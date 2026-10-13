"""Visualiza os resultados da distributividade e compara o custo operacional."""

from pathlib import Path


def _validar_matrizes(matriz_esquerda, matriz_direita):
    """Confere se as matrizes são não vazias, retangulares e têm a mesma forma."""
    if not matriz_esquerda or not matriz_direita:
        raise ValueError("As matrizes resultado não podem estar vazias.")

    colunas_esquerda = len(matriz_esquerda[0])
    colunas_direita = len(matriz_direita[0])

    if colunas_esquerda == 0 or colunas_direita == 0:
        raise ValueError("As matrizes resultado não podem ter linhas vazias.")

    if (
        len(matriz_esquerda) != len(matriz_direita)
        or colunas_esquerda != colunas_direita
    ):
        raise ValueError(
            "As matrizes resultado precisam ter as mesmas dimensões "
            "para serem comparadas."
        )

    if any(len(linha) != colunas_esquerda for linha in matriz_esquerda):
        raise ValueError("A matriz A(B + C) não é retangular.")

    if any(len(linha) != colunas_direita for linha in matriz_direita):
        raise ValueError("A matriz AB + AC não é retangular.")


def _vetor_grafico(linha, dimensao):
    """Limita o vetor às componentes que cabem no gráfico 2D/3D."""
    vetor = [float(valor) for valor in linha[:dimensao]]
    if dimensao == 2 and len(vetor) == 1:
        vetor.append(0.0)
    return vetor


def _configurar_eixos_vetoriais(ax, vetores, dimensao, titulo):
    """Configura limites, rótulos e grade do painel de vetores."""
    valores = [
        abs(componente)
        for vetor in vetores
        for componente in vetor[:dimensao]
    ]
    limite = max(max(valores, default=0.0) * 1.2, 1.0)

    ax.set_title(titulo)
    ax.set_xlabel("Componente 1")
    ax.set_ylabel("Componente 2")
    ax.set_xlim(-limite, limite)
    ax.set_ylim(-limite, limite)
    ax.axhline(0, color="gray", linewidth=0.6, alpha=0.7)
    ax.axvline(0, color="gray", linewidth=0.6, alpha=0.7)
    ax.grid(True, linestyle=":", alpha=0.5)

    if dimensao == 3:
        ax.set_zlabel("Componente 3")
        ax.set_zlim(-limite, limite)
        ax.set_box_aspect((1, 1, 1))
    else:
        ax.set_aspect("equal", adjustable="box")


def _desenhar_vetor(ax, vetor, dimensao, cor, desenhar_seta=True,
                    desenhar_tracado=False, marcador_aberto=False):
    """Desenha um vetor 2D/3D como seta e/ou linha tracejada."""
    if dimensao == 3:
        x, y, z = vetor[:3]
        if desenhar_tracado:
            ax.plot(
                [0, x], [0, y], [0, z],
                linestyle="--", color=cor, linewidth=1.7, alpha=0.9,
            )
        if desenhar_seta:
            ax.quiver(
                0, 0, 0, x, y, z,
                color=cor, arrow_length_ratio=0.12, normalize=False,
            )
        if marcador_aberto:
            ax.scatter(
                [x], [y], [z], facecolors="none", edgecolors=[cor],
                s=45, depthshade=False,
            )
    else:
        x, y = vetor[:2]
        if desenhar_tracado:
            ax.plot(
                [0, x], [0, y], linestyle="--", color=cor,
                linewidth=1.7, alpha=0.9,
            )
        if desenhar_seta:
            ax.quiver(
                0, 0, x, y,
                angles="xy", scale_units="xy", scale=1,
                color=cor, alpha=0.95,
            )
        if marcador_aberto:
            ax.scatter(
                [x], [y], facecolors="none", edgecolors=[cor], s=45,
            )


def _desenhar_comparacao_operacoes(ax, contador_esquerdo, contador_direito):
    """Compara quantidades de somas e multiplicações em barras agrupadas."""
    categorias = ["Somas", "Multiplicações"]
    valores_esquerda = [
        contador_esquerdo.somas,
        contador_esquerdo.multiplicacoes,
    ]
    valores_direita = [
        contador_direito.somas,
        contador_direito.multiplicacoes,
    ]

    import numpy as np

    posicoes = np.arange(len(categorias))
    largura = 0.34

    barras_esquerda = ax.bar(
        posicoes - largura / 2,
        valores_esquerda,
        largura,
        label="A(B + C)",
        color="tab:blue",
    )
    barras_direita = ax.bar(
        posicoes + largura / 2,
        valores_direita,
        largura,
        label="AB + AC",
        color="tab:orange",
    )

    ax.bar_label(barras_esquerda, padding=3, fontsize=9)
    ax.bar_label(barras_direita, padding=3, fontsize=9)

    # Destaca quanto a forma AB + AC acrescenta em cada categoria.
    for indice, (esquerda, direita) in enumerate(
        zip(valores_esquerda, valores_direita)
    ):
        diferenca = direita - esquerda
        topo = max(esquerda, direita)
        sinal = "+" if diferenca > 0 else ""
        ax.annotate(
            f"Diferença: {sinal}{diferenca}",
            xy=(posicoes[indice], topo),
            xytext=(0, 22),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
            color="black",
        )

    maior_valor = max(valores_esquerda + valores_direita, default=0)
    ax.set_ylim(0, max(1, maior_valor * 1.35 + 3))
    ax.set_xticks(posicoes, categorias)
    ax.set_ylabel("Quantidade de operações escalares")
    ax.set_title("Comparação do número de operações")
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)
    ax.legend(fontsize="small")


def desenhar_comparacao_resultados(
    resultado_esquerdo,
    resultado_direito,
    contador_esquerdo,
    contador_direito,
):
    """Desenha os resultados sobrepostos e compara suas contagens de operações.

    O primeiro painel representa cada linha das matrizes resultado como um
    vetor. O segundo painel compara a quantidade de somas e multiplicações
    realizadas por cada forma e anota a diferença de contagem.
    """
    try:
        import matplotlib.pyplot as plt
        from matplotlib.lines import Line2D
    except ImportError:
        print(
            "\nNão foi possível gerar a visualização: Matplotlib não está instalado."
            "\nInstale-o com: python -m pip install matplotlib"
        )
        return

    _validar_matrizes(resultado_esquerdo, resultado_direito)

    quantidade_colunas = len(resultado_esquerdo[0])
    dimensao = 3 if quantidade_colunas >= 3 else 2

    vetores_esquerdo = [
        _vetor_grafico(linha, dimensao) for linha in resultado_esquerdo
    ]
    vetores_direito = [
        _vetor_grafico(linha, dimensao) for linha in resultado_direito
    ]

    fig = plt.figure(figsize=(14, 6))
    if dimensao == 3:
        ax_vetores = fig.add_subplot(1, 2, 1, projection="3d")
    else:
        ax_vetores = fig.add_subplot(1, 2, 1)
    ax_operacoes = fig.add_subplot(1, 2, 2)

    # Painel 1: seta sólida para a forma esquerda e traço para a direita.
    for vetor_esq, vetor_dir in zip(vetores_esquerdo, vetores_direito):
        _desenhar_vetor(
            ax_vetores,
            vetor_esq,
            dimensao,
            "tab:blue",
            desenhar_seta=True,
        )
        _desenhar_vetor(
            ax_vetores,
            vetor_dir,
            dimensao,
            "tab:orange",
            desenhar_seta=False,
            desenhar_tracado=True,
            marcador_aberto=True,
        )

    _configurar_eixos_vetoriais(
        ax_vetores,
        vetores_esquerdo + vetores_direito,
        dimensao,
        "Resultados sobrepostos por linha",
    )
    ax_vetores.legend(
        handles=[
            Line2D(
                [0], [0], color="tab:blue", linestyle="-", marker=">",
                label="A(B + C)",
            ),
            Line2D(
                [0], [0], color="tab:orange", linestyle="--", marker="o",
                markerfacecolor="none", label="AB + AC",
            ),
        ],
        loc="best",
        fontsize="small",
    )

    # Painel 2: compara as contagens de operações, não diferenças de floats.
    _desenhar_comparacao_operacoes(
        ax_operacoes, contador_esquerdo, contador_direito
    )

    fig.suptitle(
        "Propriedade distributiva: resultados e custo operacional",
        fontsize=14,
    )
    fig.tight_layout()

    caminho_saida = Path(__file__).with_name("comparacao_resultados.png")
    fig.savefig(caminho_saida, dpi=200, bbox_inches="tight")

    diferenca_somas = contador_direito.somas - contador_esquerdo.somas
    diferenca_multiplicacoes = (
        contador_direito.multiplicacoes - contador_esquerdo.multiplicacoes
    )

    print("\n--- Visualização dos resultados ---")
    print(
        "Painel 1: linhas correspondentes dos resultados sobrepostas "
        "(seta azul versus linha tracejada laranja)."
    )
    print(
        "Painel 2: quantidade de somas e multiplicações em cada forma, "
        "com a diferença de contagem destacada."
    )
    print(
        "Diferença de somas (AB + AC menos A(B + C)): "
        f"{diferenca_somas:+d}"
    )
    print(
        "Diferença de multiplicações (AB + AC menos A(B + C)): "
        f"{diferenca_multiplicacoes:+d}"
    )
    if quantidade_colunas > 3:
        print(
            "Aviso: o gráfico vetorial mostra apenas as três primeiras "
            "componentes de cada linha; o cálculo matricial completo não foi alterado."
        )
    print(f"Imagem salva em: {caminho_saida}")

    plt.show()
