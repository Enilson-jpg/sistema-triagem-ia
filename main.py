import modulo1_rede_bayesiana as m1
import modulo2_busca_a_estrela as m2

def executar_sistema_triagem():
    print("--- INICIALIZANDO SISTEMA DE TRIAGEM INTELIGENTE ---")
    rede = m1.criar_rede_bayesiana()
    
    # Base de pacientes para teste
    pacientes_sintomas = [
        {"id": 1, "nome": "Ana", "tempo_espera": 10, "sintomas": {'Febre': 1, 'Saturacao_O2': 2, 'Pressao_Arterial': 1, 'Frequencia_Cardiaca': 1, 'Nivel_Dor': 1, 'Idade_Doenca': 1}},
        {"id": 2, "nome": "Bruno", "tempo_espera": 30, "sintomas": {'Febre': 0, 'Saturacao_O2': 0, 'Pressao_Arterial': 1, 'Frequencia_Cardiaca': 0, 'Nivel_Dor': 0, 'Idade_Doenca': 1}},
        {"id": 3, "nome": "Carla", "tempo_espera": 5, "sintomas": {'Febre': 0, 'Saturacao_O2': 0, 'Pressao_Arterial': 0, 'Frequencia_Cardiaca': 0, 'Nivel_Dor': 0, 'Idade_Doenca': 0}}
    ]
    
    fila_pacientes = []
    
    print("\n1. Avaliando pacientes na Rede Bayesiana (Módulo 1)...")
    for p_data in pacientes_sintomas:
        prob = m1.inferir_gravidade(rede, p_data["sintomas"])
        prob_alta = prob.values[2] # Extrai P(Gravidade = Alta)
        
        novo_paciente = m2.Paciente(p_data["id"], p_data["nome"], prob_alta, p_data["tempo_espera"])
        fila_pacientes.append(novo_paciente)
        print(f" - {p_data['nome']} avaliado(a): P(Gravidade Alta) = {prob_alta:.2f}")
        
    print("\n2. Calculando Ordem Ótima de Atendimento com A* (Módulo 2)...")
    ordem, custo = m2.estrategia_a_estrela(fila_pacientes)
    
    print(f"\n=== RESULTADO FINAL - ORDEM DE CHAMADA ===")
    for i, p in enumerate(ordem):
        print(f"{i+1}º a ser atendido -> {p.nome}")
    print(f"Risco Acumulado Total: {custo:.2f}")

if __name__ == "__main__":
    executar_sistema_triagem()