"""Executa e compara os dois lados da propriedade distributiva."""

from contador import ContadorOperacoes
from visualizacao_resultados import desenhar_comparacao_resultados
from matrizes import (
    exibir_matriz,
    matrizes_iguais,
    multiplicar_matrizes,
    somar_matrizes,
)


def executar(A, B, C, mostrar_matrizes=True):
    """Calcula A(B+C) e AB+AC, conta operações e apresenta a comparação."""
    # Lado esquerdo: A(B + C)
    contador_esquerdo = ContadorOperacoes()
    B_mais_C = somar_matrizes(B, C, contador_esquerdo)
    resultado_esquerdo = multiplicar_matrizes(A, B_mais_C, contador_esquerdo)

    # Lado direito: AB + AC
    contador_direito = ContadorOperacoes()
    AB = multiplicar_matrizes(A, B, contador_direito)
    AC = multiplicar_matrizes(A, C, contador_direito)
    resultado_direito = somar_matrizes(AB, AC, contador_direito)

    print("\n" + "=" * 60)
    print("RESULTADOS")
    print("=" * 60)
    print("\nPropriedade verificada: A(B + C) = AB + AC")

    print("\n--- A(B + C) ---")
    _exibir_custo(contador_esquerdo)

    print("\n--- AB + AC ---")
    _exibir_custo(contador_direito)

    print("\n--- Verificação matemática ---")
    if matrizes_iguais(resultado_esquerdo, resultado_direito):
        print("Os resultados são iguais (considerando a tolerância numérica).")
    else:
        print("Os resultados diferem além da tolerância numérica.")

    print("\n--- Comparação de custo ---")
    custo_esquerdo = contador_esquerdo.custo_total
    custo_direito = contador_direito.custo_total

    if custo_esquerdo < custo_direito:
        economia = custo_direito - custo_esquerdo
        percentual = economia / custo_direito * 100
        print("A(B + C) tem menor custo no modelo adotado.")
        print(f"Diferença: {economia} unidades de custo ({percentual:.2f}%).")
    elif custo_direito < custo_esquerdo:
        economia = custo_esquerdo - custo_direito
        percentual = economia / custo_esquerdo * 100
        print("AB + AC tem menor custo no modelo adotado.")
        print(f"Diferença: {economia} unidades de custo ({percentual:.2f}%).")
    else:
        print("As duas formas têm o mesmo custo no modelo adotado.")

    if mostrar_matrizes:
        exibir_matriz("A(B + C)", resultado_esquerdo)
        exibir_matriz("AB + AC", resultado_direito)

    print(
        "\nNota: o custo é um modelo simplificado (1 unidade por soma e por "
        "multiplicação); não é uma medição real dos ciclos da CPU."
    )

    # Compara visualmente as linhas correspondentes e mostra a diferença
    # entre as duas matrizes resultado.
    desenhar_comparacao_resultados(
        resultado_esquerdo,
        resultado_direito,
        contador_esquerdo,
        contador_direito,
    )


def _exibir_custo(contador):
    print(f"Somas:                  {contador.somas}")
    print(f"Multiplicações:         {contador.multiplicacoes}")
    print(f"Custo estimado:         {contador.custo_total} unidades")
