"""Contagem e modelo simplificado de custo das operações."""

# Pesos arbitrários usados para comparar as expressões.
# Não representam uma medição real dos ciclos da CPU.
CUSTO_SOMA = 1
CUSTO_MULTIPLICACAO = 1


class ContadorOperacoes:
    """Armazena a quantidade de operações escalares executadas."""

    def __init__(self):
        self.somas = 0
        self.multiplicacoes = 0

    @property
    def custo_total(self):
        return (
            self.somas * CUSTO_SOMA
            + self.multiplicacoes * CUSTO_MULTIPLICACAO
        )
