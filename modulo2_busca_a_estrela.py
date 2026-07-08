import heapq

class Paciente:
    def __init__(self, id_paciente, nome, prob_alta, tempo_espera):
        self.id = id_paciente
        self.nome = nome
        self.prob_alta = prob_alta
        self.tempo_espera = tempo_espera

    def calcular_risco(self):
        # risco(paciente) = P(gravidade_alta) * tempo_esperando
        return self.prob_alta * self.tempo_espera

class EstadoFila:
    def __init__(self, fila_espera, custo_acumulado, ordem_atendimento):
        self.fila_espera = fila_espera
        self.custo_acumulado = custo_acumulado
        self.ordem_atendimento = ordem_atendimento

    def heuristica(self):
        # h(n): soma dos riscos atuais
        return sum(p.calcular_risco() for p in self.fila_espera)

    def f_cost(self):
        # f(n) = g(n) + h(n)
        return self.custo_acumulado + self.heuristica()

    def __lt__(self, other):
        return self.f_cost() < other.f_cost()

def simular_custo_sequencia(ordem_pacientes, tempo_atendimento=10):
    custo_total = 0
    pacientes = [Paciente(p.id, p.nome, p.prob_alta, p.tempo_espera) for p in ordem_pacientes]
    
    for i in range(len(pacientes)):
        pacientes_restantes = pacientes[i+1:]
        custo_total += sum(p.calcular_risco() for p in pacientes_restantes)
        
        for p in pacientes_restantes:
            p.tempo_espera += tempo_atendimento
            
    return custo_total

def estrategia_fifo(pacientes):
    ordem = sorted(pacientes, key=lambda p: p.tempo_espera, reverse=True)
    return ordem, simular_custo_sequencia(ordem)

def estrategia_gulosa(pacientes):
    ordem = sorted(pacientes, key=lambda p: p.prob_alta, reverse=True)
    return ordem, simular_custo_sequencia(ordem)

def estrategia_a_estrela(pacientes_iniciais, tempo_atendimento=10):
    open_set = []
    pacientes_copia = [Paciente(p.id, p.nome, p.prob_alta, p.tempo_espera) for p in pacientes_iniciais]
    estado_inicial = EstadoFila(pacientes_copia, 0, [])
    
    contador = 0
    heapq.heappush(open_set, (estado_inicial.f_cost(), contador, estado_inicial))
    
    while open_set:
        _, _, estado_atual = heapq.heappop(open_set)
        
        if not estado_atual.fila_espera:
            return estado_atual.ordem_atendimento, estado_atual.custo_acumulado
            
        for i, paciente_escolhido in enumerate(estado_atual.fila_espera):
            nova_fila = estado_atual.fila_espera[:i] + estado_atual.fila_espera[i+1:]
            
            custo_rodada = sum(p.calcular_risco() for p in nova_fila)
            novo_custo_acumulado = estado_atual.custo_acumulado + custo_rodada
            
            nova_fila_atualizada = [
                Paciente(p.id, p.nome, p.prob_alta, p.tempo_espera + tempo_atendimento)
                for p in nova_fila
            ]
                
            nova_ordem = estado_atual.ordem_atendimento + [paciente_escolhido]
            novo_estado = EstadoFila(nova_fila_atualizada, novo_custo_acumulado, nova_ordem)
            
            contador += 1
            heapq.heappush(open_set, (novo_estado.f_cost(), contador, novo_estado))

    return [], 0

if __name__ == "__main__":
    pacientes_teste = [
        Paciente(1, "Ana", 0.85, 10),
        Paciente(2, "Bruno", 0.60, 30),
        Paciente(3, "Carla", 0.20, 5)
    ]
    
    print("--- RESULTADOS DOS EXPERIMENTOS ---\n")
    
    ordem_fifo, custo_fifo = estrategia_fifo(pacientes_teste)
    print(f"Estratégia FIFO:\nOrdem: {[p.nome for p in ordem_fifo]}\nCusto: {custo_fifo:.1f}\n")
    
    ordem_gulosa, custo_gulosa = estrategia_gulosa(pacientes_teste)
    print(f"Estratégia Gulosa:\nOrdem: {[p.nome for p in ordem_gulosa]}\nCusto: {custo_gulosa:.1f}\n")
    
    ordem_a_estrela, custo_a_estrela = estrategia_a_estrela(pacientes_teste)
    print(f"Estratégia A*:\nOrdem: {[p.nome for p in ordem_a_estrela]}\nCusto: {custo_a_estrela:.1f}\n")