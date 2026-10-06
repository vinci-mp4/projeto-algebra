import random
import math


# ============================================================
# CONFIGURAÇÃO DO MODELO DE CUSTO
# ============================================================

CUSTO_SOMA = 1
CUSTO_MULTIPLICACAO = 1


# ============================================================
# CONTADOR DE OPERAÇÕES
# ============================================================

class ContadorOperacoes:
    def __init__(self):
        self.somas = 0
        self.multiplicacoes = 0

    @property
    def custo_total(self):
        return (
            self.somas * CUSTO_SOMA
            + self.multiplicacoes * CUSTO_MULTIPLICACAO
        )


# ============================================================
# LEITURA DE DIMENSÕES
# ============================================================

def ler_dimensoes(nome):
    while True:
        entrada = input(
            f"Dimensões de {nome} (linhas colunas): "
        ).strip().split()

        if len(entrada) != 2:
            print("Digite exatamente duas dimensões.")
            continue

        try:
            linhas = int(entrada[0])
            colunas = int(entrada[1])

            if linhas <= 0 or colunas <= 0:
                print("As dimensões devem ser maiores que zero.")
                continue

            return linhas, colunas

        except ValueError:
            print("Digite números inteiros válidos.")


# ============================================================
# VALIDAÇÃO DAS DIMENSÕES
# ============================================================

def validar_dimensoes(A_dim, B_dim, C_dim):
    a_linhas, a_colunas = A_dim
    b_linhas, b_colunas = B_dim
    c_linhas, c_colunas = C_dim

    # B e C precisam poder ser somadas
    if B_dim != C_dim:
        return False, "B e C precisam ter as mesmas dimensões."

    # A(B + C)
    # A: m x n
    # B+C: n x p
    if a_colunas != b_linhas:
        return False, (
            "O número de colunas de A deve ser igual "
            "ao número de linhas de B e C."
        )

    return True, ""


# ============================================================
# LEITURA DE MATRIZ MANUAL
# ============================================================

def ler_matriz_manual(nome, linhas, colunas):
    print(f"\nDigite a matriz {nome}, uma linha por vez.")

    matriz = []

    for i in range(linhas):
        while True:
            entrada = input(f"{nome}[{i + 1}]: ").strip().split()

            if len(entrada) != colunas:
                print(
                    f"Essa linha deve possuir exatamente "
                    f"{colunas} valores."
                )
                continue

            try:
                linha = [float(valor) for valor in entrada]
                matriz.append(linha)
                break

            except ValueError:
                print("Todos os valores devem ser números.")

    return matriz


# ============================================================
# GERAÇÃO AUTOMÁTICA DE MATRIZ
# ============================================================

def gerar_matriz(linhas, colunas, minimo, maximo):
    return [
        [
            random.uniform(minimo, maximo)
            for _ in range(colunas)
        ]
        for _ in range(linhas)
    ]


# ============================================================
# SOMA DE MATRIZES
# ============================================================

def somar_matrizes(A, B, contador):
    linhas = len(A)
    colunas = len(A[0])

    resultado = []

    for i in range(linhas):
        linha = []

        for j in range(colunas):
            linha.append(A[i][j] + B[i][j])
            contador.somas += 1

        resultado.append(linha)

    return resultado


# ============================================================
# MULTIPLICAÇÃO DE MATRIZES
# ============================================================

def multiplicar_matrizes(A, B, contador):
    linhas_A = len(A)
    colunas_A = len(A[0])
    linhas_B = len(B)
    colunas_B = len(B[0])

    if colunas_A != linhas_B:
        raise ValueError(
            "Matrizes incompatíveis para multiplicação."
        )

    resultado = []

    for i in range(linhas_A):
        linha = []

        for j in range(colunas_B):
            soma = 0.0

            for k in range(colunas_A):
                produto = A[i][k] * B[k][j]
                contador.multiplicacoes += 1

                # A última multiplicação não precisa de uma
                # soma adicional se estivermos acumulando.
                if k == 0:
                    soma = produto
                else:
                    soma += produto
                    contador.somas += 1

            linha.append(soma)

        resultado.append(linha)

    return resultado


# ============================================================
# COMPARAÇÃO DE MATRIZES
# ============================================================

def matrizes_iguais(A, B, tolerancia=1e-9):
    if len(A) != len(B):
        return False

    if len(A[0]) != len(B[0]):
        return False

    for i in range(len(A)):
        for j in range(len(A[0])):
            if not math.isclose(
                A[i][j],
                B[i][j],
                rel_tol=tolerancia,
                abs_tol=tolerancia
            ):
                return False

    return True


# ============================================================
# EXIBIÇÃO DE MATRIZ
# ============================================================

def exibir_matriz(nome, matriz):
    print(f"\n{nome} =")

    for linha in matriz:
        print(
            " ".join(
                f"{valor:.4f}"
                for valor in linha
            )
        )


# ============================================================
# EXECUÇÃO DA PROPRIEDADE DISTRIBUTIVA
# ============================================================

def executar(A, B, C):
    # --------------------------------------------------------
    # FORMA 1: A(B + C)
    # --------------------------------------------------------

    contador_1 = ContadorOperacoes()

    B_mais_C = somar_matrizes(B, C, contador_1)
    resultado_1 = multiplicar_matrizes(
        A,
        B_mais_C,
        contador_1
    )

    # --------------------------------------------------------
    # FORMA 2: AB + AC
    # --------------------------------------------------------

    contador_2 = ContadorOperacoes()

    AB = multiplicar_matrizes(
        A,
        B,
        contador_2
    )

    AC = multiplicar_matrizes(
        A,
        C,
        contador_2
    )

    resultado_2 = somar_matrizes(
        AB,
        AC,
        contador_2
    )

    # --------------------------------------------------------
    # RESULTADOS
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("RESULTADOS")
    print("=" * 60)

    print("\nPropriedade:")
    print("A(B + C) = AB + AC")

    print("\n--- A(B + C) ---")
    print(f"Somas:              {contador_1.somas}")
    print(f"Multiplicações:     {contador_1.multiplicacoes}")
    print(f"Custo total:        {contador_1.custo_total} ciclos")

    print("\n--- AB + AC ---")
    print(f"Somas:              {contador_2.somas}")
    print(f"Multiplicações:     {contador_2.multiplicacoes}")
    print(f"Custo total:        {contador_2.custo_total} ciclos")

    print("\n--- Verificação ---")

    if matrizes_iguais(resultado_1, resultado_2):
        print("Os resultados são iguais.")
    else:
        print(
            "Os resultados não são exatamente iguais "
            "devido à precisão numérica."
        )

    print("\n--- Comparação de custo ---")

    if contador_1.custo_total < contador_2.custo_total:
        diferenca = (
            contador_2.custo_total
            - contador_1.custo_total
        )

        percentual = (
            diferenca
            / contador_2.custo_total
        ) * 100

        print(
            "A(B + C) é mais eficiente."
        )

        print(
            f"Economia: {diferenca} ciclos "
            f"({percentual:.2f}%)."
        )

    elif contador_2.custo_total < contador_1.custo_total:
        diferenca = (
            contador_1.custo_total
            - contador_2.custo_total
        )

        percentual = (
            diferenca
            / contador_1.custo_total
        ) * 100

        print(
            "AB + AC é mais eficiente."
        )

        print(
            f"Economia: {diferenca} ciclos "
            f"({percentual:.2f}%)."
        )

    else:
        print("As duas formas possuem o mesmo custo.")

    # --------------------------------------------------------
    # MOSTRAR MATRIZES RESULTANTES
    # --------------------------------------------------------

    exibir_matriz("A(B + C)", resultado_1)
    exibir_matriz("AB + AC", resultado_2)


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():
    while True:
        print("\n" + "=" * 60)
        print("CONTADOR DE OPERAÇÕES - MATRIZES")
        print("=" * 60)
        print("1 - Informar matrizes manualmente")
        print("2 - Gerar matrizes automaticamente")
        print("0 - Sair")

        opcao = input("\nOpção: ").strip()

        if opcao == "0":
            print("\nPrograma encerrado.")
            break

        elif opcao == "1":
            # ------------------------------------------------
            # ENTRADA MANUAL
            # ------------------------------------------------

            while True:
                A_dim = ler_dimensoes("A")
                B_dim = ler_dimensoes("B")
                C_dim = ler_dimensoes("C")

                valido, mensagem = validar_dimensoes(
                    A_dim,
                    B_dim,
                    C_dim
                )

                if valido:
                    break

                print(f"\nErro: {mensagem}")
                print("Informe as dimensões novamente.\n")

            A = ler_matriz_manual(
                "A",
                A_dim[0],
                A_dim[1]
            )

            B = ler_matriz_manual(
                "B",
                B_dim[0],
                B_dim[1]
            )

            C = ler_matriz_manual(
                "C",
                C_dim[0],
                C_dim[1]
            )

            executar(A, B, C)

        elif opcao == "2":
            # ------------------------------------------------
            # GERAÇÃO AUTOMÁTICA
            # ------------------------------------------------

            while True:
                A_dim = ler_dimensoes("A")
                B_dim = ler_dimensoes("B")
                C_dim = ler_dimensoes("C")

                valido, mensagem = validar_dimensoes(
                    A_dim,
                    B_dim,
                    C_dim
                )

                if valido:
                    break

                print(f"\nErro: {mensagem}")
                print("Informe as dimensões novamente.\n")

            while True:
                entrada = input(
                    "\nIntervalo dos valores aleatórios "
                    "(mínimo máximo): "
                ).strip().split()

                if len(entrada) != 2:
                    print(
                        "Digite exatamente dois valores."
                    )
                    continue

                try:
                    minimo = float(entrada[0])
                    maximo = float(entrada[1])

                    if minimo > maximo:
                        print(
                            "O valor mínimo não pode ser "
                            "maior que o máximo."
                        )
                        continue

                    break

                except ValueError:
                    print("Digite valores numéricos válidos.")

            A = gerar_matriz(
                A_dim[0],
                A_dim[1],
                minimo,
                maximo
            )

            B = gerar_matriz(
                B_dim[0],
                B_dim[1],
                minimo,
                maximo
            )

            C = gerar_matriz(
                C_dim[0],
                C_dim[1],
                minimo,
                maximo
            )

            executar(A, B, C)

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()