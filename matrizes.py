"""Operações básicas e utilitários para matrizes representadas por listas."""

import math
import random


CHANCE_INTEIRO = 0.60


def gerar_valor(minimo, maximo):
    """Gera um número com no máximo uma casa decimal.

    Quando o intervalo permite os dois tipos, há 60% de chance de escolher
    um inteiro e 40% de escolher um decimal com uma casa decimal.
    Se o intervalo só permitir um dos tipos, usa o tipo disponível.
    """
    # Valores inteiros permitidos no intervalo.
    menor_inteiro = math.ceil(minimo)
    maior_inteiro = math.floor(maximo)
    tem_inteiro = menor_inteiro <= maior_inteiro

    # Representamos valores com uma casa decimal como inteiros multiplicados
    # por 10. A pequena margem evita erros de ponto flutuante nos limites.
    menor_decimo = math.ceil(minimo * 10 - 1e-9)
    maior_decimo = math.floor(maximo * 10 + 1e-9)
    quantidade_decimos = max(0, maior_decimo - menor_decimo + 1)

    # Exclui múltiplos de 10, que corresponderiam a números inteiros.
    if quantidade_decimos:
        quantidade_inteiros_em_decimos = (
            maior_decimo // 10 - (menor_decimo - 1) // 10
        )
    else:
        quantidade_inteiros_em_decimos = 0

    tem_decimal = quantidade_decimos > quantidade_inteiros_em_decimos

    if not tem_inteiro and not tem_decimal:
        raise ValueError(
            "O intervalo precisa conter pelo menos um valor com no máximo "
            "uma casa decimal."
        )

    escolher_inteiro = random.random() < CHANCE_INTEIRO

    if escolher_inteiro and tem_inteiro:
        return float(random.randint(menor_inteiro, maior_inteiro))

    if tem_decimal and (not escolher_inteiro or not tem_inteiro):
        while True:
            decimos = random.randint(menor_decimo, maior_decimo)
            if decimos % 10 != 0:
                return decimos / 10

    # Caso o intervalo só contenha inteiros, usa um deles.
    return float(random.randint(menor_inteiro, maior_inteiro))


def gerar_matriz(linhas, colunas, minimo, maximo):
    """Gera uma matriz com inteiros e decimais de uma casa no intervalo."""
    return [
        [gerar_valor(minimo, maximo) for _ in range(colunas)]
        for _ in range(linhas)
    ]


def somar_matrizes(A, B, contador):
    """Soma duas matrizes e atualiza o contador de operações."""
    if len(A) != len(B) or any(len(a) != len(b) for a, b in zip(A, B)):
        raise ValueError("As matrizes precisam ter as mesmas dimensões para serem somadas.")

    resultado = []

    for linha_a, linha_b in zip(A, B):
        linha_resultado = []
        for a, b in zip(linha_a, linha_b):
            linha_resultado.append(a + b)
            contador.somas += 1
        resultado.append(linha_resultado)

    return resultado


def multiplicar_matrizes(A, B, contador):
    """Multiplica duas matrizes e conta as operações escalares.

    Para cada elemento do resultado, são contadas n multiplicações e n-1
    somas, evitando contar uma soma inicial com zero.
    """
    if not A or not B or not A[0] or not B[0]:
        raise ValueError("As matrizes não podem estar vazias.")

    linhas_A = len(A)
    colunas_A = len(A[0])
    linhas_B = len(B)
    colunas_B = len(B[0])

    if any(len(linha) != colunas_A for linha in A):
        raise ValueError("A matriz A possui linhas com tamanhos diferentes.")
    if any(len(linha) != colunas_B for linha in B):
        raise ValueError("A matriz B possui linhas com tamanhos diferentes.")
    if colunas_A != linhas_B:
        raise ValueError("Matrizes incompatíveis para multiplicação.")

    resultado = []

    for i in range(linhas_A):
        linha_resultado = []

        for j in range(colunas_B):
            acumulado = None

            for k in range(colunas_A):
                produto = A[i][k] * B[k][j]
                contador.multiplicacoes += 1

                if k == 0:
                    acumulado = produto
                else:
                    acumulado += produto
                    contador.somas += 1

            linha_resultado.append(acumulado)

        resultado.append(linha_resultado)

    return resultado


def matrizes_iguais(A, B, tolerancia=1e-9):
    """Compara matrizes com tolerância para diferenças de ponto flutuante."""
    if len(A) != len(B):
        return False

    for linha_a, linha_b in zip(A, B):
        if len(linha_a) != len(linha_b):
            return False
        for a, b in zip(linha_a, linha_b):
            if not math.isclose(
                a, b, rel_tol=tolerancia, abs_tol=tolerancia
            ):
                return False

    return True


def exibir_matriz(nome, matriz, casas_decimais=4, inteiros_sem_decimal=False):
    """Imprime uma matriz; permite exibir inteiros sem parte decimal."""
    print(f"\n{nome} =")

    def formatar(valor):
        if inteiros_sem_decimal and float(valor).is_integer():
            return str(int(valor))
        return f"{valor:.{casas_decimais}f}"

    for linha in matriz:
        print(" ".join(formatar(valor) for valor in linha))
