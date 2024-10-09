import numpy as np
import igraph as ig
from model_gen.model_generator_ns import ModelGeneratorNS
from model_gen.dynamic_manufacturing import DynamicManufacturing

# Definir parâmetros
n = 10  # número de estações de trabalho
s = 5  # número de etapas de produção
seed = 42  # semente para gerar números aleatórios
initial_buffer = 100  # quantidade inicial de buffer
mean_production_time = 10  # tempo médio de produção

# Criar um gerador de números aleatórios
rng = np.random.default_rng(seed=seed)

# Inicializar o gerador de modelo
model_gen = ModelGeneratorNS(n=n, s=s, rng=rng, first_step=1, last_step=2)

# Gerar o grafo da rede de produção
work_stations, production_edges, vertex_attr = model_gen.generate_graph()

# Converter os dados para um objeto Graph do igraph
# AQUI ESTÁ A ALTERAÇÃO PARA CRIAR O GRAFO DIRECIONADO
g = ig.Graph(directed=True)
g.add_vertices(n)
g.add_edges(production_edges)
g.vs["label"] = vertex_attr["label"]
g.vs["production_rate"] = vertex_attr["production_rate"]
g.vs["failure_rate"] = vertex_attr["failure_rate"]
g.vs["buffer_size"] = vertex_attr["buffer_size"]
g.vs["production_step"] = vertex_attr["production_step"]

# Inicializar a simulação dinâmica
simulator = DynamicManufacturing(network=g, seed=seed, rng=rng, initial_buffer=initial_buffer, mean_production_time=mean_production_time)

# Abrir arquivos de saída para log
with open('output.csv', 'w') as output, open('log.csv', 'w') as log, open('event_log.csv', 'w') as event_log:
    # Rodar a simulação por um número específico de iterações
    num_iterations = 100
    for _ in range(num_iterations):
        total_production, starved, blocked, working, state_array = simulator.iterate(output=output, write2file=True, event_log=event_log, log=log)

        # Exibir resultados da iteração
        print(f"Iteração {_+1}: Produção Total = {total_production}, Starved = {starved}, Blocked = {blocked}, Working = {working}")

print("Simulação completa.")
