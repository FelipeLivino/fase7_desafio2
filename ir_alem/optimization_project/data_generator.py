import json
import random
import os

#Gera dados sintéticos para otimização de recursos agrícolas.
def generate_farm_data(num_items=50, max_cost=100, seed=42, output_file="inputs/farm_data.json"):

    random.seed(seed)
    
    item_types = ["Fertilizante", "Pesticida", "Variedade_Sementes", "Plano_Irrigacao", "Contrato_Trabalho", "Aluguel_Maquinas"]
    data = []
    
    for i in range(num_items):
        item_type = random.choice(item_types)
        name = f"{item_type}_{i+1}"
        
        # Custo aleatório
        cost = random.randint(10, max_cost)
        
        # A produtividade está de certa forma correlacionada ao custo, mas com variações.
        # Custos mais altos geralmente significam maior produtividade, mas essa relação nem sempre é linear.
        base_productivity = cost * random.uniform(0.8, 1.5)
        productivity = int(base_productivity)
        
        data.append({
            "id": i,
            "name": name,
            "cost": cost,
            "productivity": productivity
        })
    
    # Calcule um orçamento razoável (por exemplo, 50% do custo total)
    total_cost = sum(item['cost'] for item in data)
    budget = int(total_cost * 0.5)
    
    output_data = {
        "metadata": {
            "num_items": num_items,
            "seed": seed,
            "budget": budget
        },
        "items": data
    }
    
    # Garantir que o diretório exista
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=4)
    
    print(f"Dados gerados com sucesso {num_items}")
    print(f"Orçamento definido para: {budget}")
    print(f"Salvo em: {output_file}")

if __name__ == "__main__":
    # Gerar conjunto de dados padrão
    generate_farm_data(num_items=100, max_cost=100, seed=42, output_file="inputs/farm_data.json")
