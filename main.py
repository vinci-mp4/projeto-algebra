"""Ponto de entrada do contador de operações de matrizes."""

from distributiva import executar
from entrada import (
    ler_dimensoes_validas,
    ler_intervalo_aleatorio,
    ler_matriz_manual,
)
from matrizes import exibir_matriz, gerar_matriz


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

        if opcao not in ("1", "2"):
            print("Opção inválida.")
            continue

        A_dim, B_dim, C_dim = ler_dimensoes_validas()

        if opcao == "1":
            A = ler_matriz_manual("A", *A_dim)
            B = ler_matriz_manual("B", *B_dim)
            C = ler_matriz_manual("C", *C_dim)
        else:
            minimo, maximo = ler_intervalo_aleatorio()
            A = gerar_matriz(*A_dim, minimo, maximo)
            B = gerar_matriz(*B_dim, minimo, maximo)
            C = gerar_matriz(*C_dim, minimo, maximo)

            print("\n" + "=" * 60)
            print("MATRIZES GERADAS ALEATORIAMENTE")
            print("Valores com no máximo 1 casa decimal; preferência por inteiros.")
            print("=" * 60)
            exibir_matriz("A", A, casas_decimais=1, inteiros_sem_decimal=True)
            exibir_matriz("B", B, casas_decimais=1, inteiros_sem_decimal=True)
            exibir_matriz("C", C, casas_decimais=1, inteiros_sem_decimal=True)

        executar(A, B, C)


if __name__ == "__main__":
    main()
