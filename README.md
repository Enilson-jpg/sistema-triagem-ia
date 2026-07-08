# Sistema Inteligente de Triagem em Pronto-Socorro 🏥🤖

Este repositório contém a implementação do Trabalho Final da disciplina de Inteligência Artificial Aplicada. [cite_start]O projeto consiste em um sistema inteligente projetado para otimizar a fila de triagem em prontos-socorros, mitigando os riscos associados à superlotação e à deterioração clínica de pacientes durante o tempo de espera[cite: 6, 7].

## 🧠 Arquitetura do Sistema

[cite_start]A solução foi dividida em dois módulos complementares que se comunicam de forma integrada[cite: 7, 10]:

### Módulo 1: Estimativa de Gravidade (Rede Bayesiana)
[cite_start]Utiliza a biblioteca `pgmpy` para modelar as incertezas clínicas[cite: 16, 46]. [cite_start]A rede bayesiana recebe seis variáveis de sinais vitais e histórico do paciente (Febre, Saturação de O2, Pressão Arterial, Frequência Cardíaca, Nível de Dor e Idade/Doença Crônica) e realiza a inferência da probabilidade do estado de gravidade (Baixa, Média ou Alta)[cite: 19, 20, 21, 22, 23, 24, 27].

### Módulo 2: Ordenação da Fila (Algoritmo A*)
Modela a fila de espera como um problema de busca em espaço de estados[cite: 51, 52, 54]. O algoritmo A* consome a probabilidade de gravidade gerada no Módulo 1 para calcular o **Risco de Deterioração** individual[cite: 63, 97]. [cite_start]Utilizando uma heurística admissível (a soma dos riscos atuais da fila), o algoritmo encontra a sequência ótima de atendimento que minimiza o dano total causado pela espera[cite: 83, 85, 87].

---

## ⚙️ Pré-requisitos e Instalação

Certifique-se de ter o Python 3.x instalado em sua máquina. Para garantir que todas as bibliotecas funcionem corretamente, recomenda-se o uso de um ambiente virtual (`venv`).

Instale as dependências necessárias executando o comando abaixo no terminal:

```bash
pip install pgmpy networkx pandas numpy