import json
import matplotlib.pyplot as plt
from genetic_algorithm import GeneticAlgorithm

def load_data(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data['items'], data['metadata']['budget']

def run_experiments():
    items, budget = load_data('inputs/farm_data.json')
    
    print(f"Carregado {len(items)} items. Orçamento: {budget}")
    
    # Configuração 1: Baseline
    print("\n--- Executando GA de linha de base ---")
    ga_baseline = GeneticAlgorithm(
        items, budget,
        pop_size=100,
        generations=100,
        selection_method='roulette',
        crossover_method='single_point',
        mutation_method='bit_flip',
        seed=42
    )
    res_baseline = ga_baseline.run()
    print(f"Baseline melhor treinamento: {res_baseline['best_fitness']}")
    print(f"Baseline tempo de execução: {res_baseline['execution_time']:.4f}s")
    
    # Configuração 2: Modificada ("Ir Além")
    print("\n--- Executando GA Modificado ---")
    ga_modified = GeneticAlgorithm(
        items, budget,
        pop_size=100,
        generations=100,
        selection_method='tournament',
        crossover_method='uniform',
        mutation_method='swap',
        seed=42
    )
    res_modified = ga_modified.run()
    print(f"Modificado melhor treinamento: {res_modified['best_fitness']}")
    print(f"Modificado tempo de execução: {res_modified['execution_time']:.4f}s")
    
    # Comparison
    print("\n--- Comparação ---")
    diff_fitness = res_modified['best_fitness'] - res_baseline['best_fitness']
    print(f"Melhoria de treinamento: {diff_fitness}")
    
    # Plotting (Optional, just saving to file)
    plt.figure(figsize=(10, 6))
    plt.plot([x['best_fitness'] for x in res_baseline['history']], label='Baseline')
    plt.plot([x['best_fitness'] for x in res_modified['history']], label='Modificado')
    plt.title('Convergência de Algoritmos Genéticos')
    plt.xlabel('Geração')
    plt.ylabel('Melhor Treinamento')
    plt.legend()
    plt.grid(True)
    plt.savefig('convergence_plot.png')
    print("Grafico salvo em convergence_plot.png")

if __name__ == "__main__":
    run_experiments()
