from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import itertools
import numpy as np

def criar_rede_bayesiana():
    # Estrutura da rede
    modelo = DiscreteBayesianNetwork([
        ('Febre', 'Gravidade'),
        ('Saturacao_O2', 'Gravidade'),
        ('Pressao_Arterial', 'Gravidade'),
        ('Frequencia_Cardiaca', 'Gravidade'),
        ('Nivel_Dor', 'Gravidade'),
        ('Idade_Doenca', 'Gravidade')
    ])

    # CPTs para Variáveis Binárias: 0 (Normal), 1 (Anormal)
    cpd_febre = TabularCPD(variable='Febre', variable_card=2, values=[[0.7], [0.3]])
    cpd_pressao = TabularCPD(variable='Pressao_Arterial', variable_card=2, values=[[0.8], [0.2]])
    cpd_freq = TabularCPD(variable='Frequencia_Cardiaca', variable_card=2, values=[[0.8], [0.2]])
    cpd_dor = TabularCPD(variable='Nivel_Dor', variable_card=2, values=[[0.6], [0.4]])
    cpd_idade = TabularCPD(variable='Idade_Doenca', variable_card=2, values=[[0.5], [0.5]])
    
    # CPT Saturação: 0 (>= 95%), 1 (90-94%), 2 (< 90%)
    cpd_saturacao = TabularCPD(variable='Saturacao_O2', variable_card=3, values=[[0.7], [0.2], [0.1]])

    # Geração dinâmica da CPT de Gravidade: 0 (Baixa), 1 (Média), 2 (Alta)
    gravidade_probs = []
    
    for f, s, p, fc, nd, id in itertools.product([0, 1], [0, 1, 2], [0, 1], [0, 1], [0, 1], [0, 1]):
        score_risco = f + s + p + fc + nd + id
        
        if score_risco <= 1:
            gravidade_probs.append([0.80, 0.15, 0.05])
        elif score_risco <= 3:
            gravidade_probs.append([0.10, 0.70, 0.20])
        else:
            gravidade_probs.append([0.05, 0.15, 0.80])

    gravidade_probs_formatada = np.array(gravidade_probs).T.tolist()

    cpd_gravidade = TabularCPD(
        variable='Gravidade', 
        variable_card=3, 
        values=gravidade_probs_formatada,
        evidence=['Febre', 'Saturacao_O2', 'Pressao_Arterial', 'Frequencia_Cardiaca', 'Nivel_Dor', 'Idade_Doenca'],
        evidence_card=[2, 3, 2, 2, 2, 2]
    )

    modelo.add_cpds(cpd_febre, cpd_saturacao, cpd_pressao, cpd_freq, cpd_dor, cpd_idade, cpd_gravidade)
    modelo.check_model()
    
    return modelo

def inferir_gravidade(modelo, evidencias):
    infer = VariableElimination(modelo)
    return infer.query(variables=['Gravidade'], evidence=evidencias)

if __name__ == "__main__":
    rede = criar_rede_bayesiana()
    print("Módulo 1: Estrutura da Rede Bayesiana montada e validada com sucesso!\n")
    
    print("Realizando inferencia de teste...")
    paciente_teste = {
        'Febre': 1, 
        'Saturacao_O2': 1, 
        'Pressao_Arterial': 1, 
        'Frequencia_Cardiaca': 0, 
        'Nivel_Dor': 1, 
        'Idade_Doenca': 1
    }
    
    probabilidades = inferir_gravidade(rede, paciente_teste)
    print("Resultado das Probabilidades (0: Baixa, 1: Média, 2: Alta):")
    print(probabilidades)