"""Funções de leitura, validação e preparação dos dados de entrada."""

import math


def ler_dimensoes(nome):
    """Lê dimensões positivas no formato: linhas colunas."""
    while True:
        entrada = input(f"Dimensões de {nome} (linhas colunas): ").strip().split()

        if len(entrada) != 2:
            print("Digite exatamente duas dimensões, separadas por espaço.")
            continue

        try:
            linhas, colunas = map(int, entrada)
            if linhas <= 0 or colunas <= 0:
                print("As dimensões devem ser maiores que zero.")
                continue
            return linhas, colunas
        except ValueError:
            print("Digite duas dimensões inteiras válidas.")


def validar_dimensoes(A_dim, B_dim, C_dim):
    """Verifica se A(B+C) e AB+AC são operações dimensionalmente válidas."""
    _, a_colunas = A_dim
    b_linhas, b_colunas = B_dim
    c_linhas, c_colunas = C_dim

    if B_dim != C_dim:
        return False, "B e C precisam ter as mesmas dimensões."

    if a_colunas != b_linhas or a_colunas != c_linhas:
        return False, (
            "O número de colunas de A deve ser igual ao número de linhas "
            "de B e C."
        )

    return True, ""


def ler_dimensoes_validas():
    """Solicita novamente as dimensões até que sejam compatíveis."""
    while True:
        print("\nInforme as dimensões das três matrizes.")
        A_dim = ler_dimensoes("A")
        B_dim = ler_dimensoes("B")
        C_dim = ler_dimensoes("C")

        valido, mensagem = validar_dimensoes(A_dim, B_dim, C_dim)
        if valido:
            return A_dim, B_dim, C_dim

        print(f"\nDimensões inválidas: {mensagem}")
        print("Informe as dimensões novamente.")


def ler_matriz_manual(nome, linhas, colunas):
    """Lê uma matriz linha por linha, aceitando números inteiros ou decimais."""
    print(f"\nDigite a matriz {nome}, uma linha por vez (valores separados por espaços).")
    matriz = []

    for i in range(linhas):
        while True:
            entrada = input(f"{nome}[{i + 1}]: ").strip().split()

            if len(entrada) != colunas:
                print(f"Essa linha deve possuir exatamente {colunas} valores.")
                continue

            try:
                linha = [float(valor) for valor in entrada]
                if not all(math.isfinite(valor) for valor in linha):
                    print("Digite apenas números finitos, como 2 ou 3.5.")
                    continue
                matriz.append(linha)
                break
            except ValueError:
                print("Todos os valores devem ser números (ex.: 2, -1.5, 3.75).")

    return matriz


def ler_intervalo_aleatorio():
    """Lê os limites dos valores usados na geração automática."""
    while True:
        entrada = input(
            "\nIntervalo dos valores aleatórios (mínimo máximo): "
        ).strip().split()

        if len(entrada) != 2:
            print("Digite exatamente dois valores, separados por espaço.")
            continue

        try:
            minimo, maximo = map(float, entrada)
            if not math.isfinite(minimo) or not math.isfinite(maximo):
                print("Os limites devem ser números finitos.")
                continue
            if minimo > maximo:
                print("O valor mínimo não pode ser maior que o máximo.")
                continue

            # A geração usa apenas valores inteiros ou décimos exatos.
            menor_decimo = math.ceil(minimo * 10 - 1e-9)
            maior_decimo = math.floor(maximo * 10 + 1e-9)
            if menor_decimo > maior_decimo:
                print(
                    "O intervalo precisa incluir algum valor com no máximo "
                    "uma casa decimal (por exemplo, 1.2 ou 3)."
                )
                continue

            return minimo, maximo
        except ValueError:
            print("Digite dois valores numéricos válidos.")
