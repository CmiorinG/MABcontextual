import random

class Usuario:
    def __init__(self, num_genero):
        self.num_genero = num_genero
        self.prob_selecao = [0.2, 0.2, 0.2, 0.2, 0.2]  #perfil ZERADO

    def escolha_usuario(self, genero):
        recompensa = random.uniform(0, 0.1)  #Recompensa a cada interação do usuário (por generoo)
        if random.random() < self.prob_selecao[genero]:
            return recompensa
        else:
            return 0

    def atualizar_probs(self, genero, recompensa):
        # Atualiza as probabilidades da escolha do usuario com base na interações ja realizadas
        total_recompensa = sum(self.prob_selecao)
        self.prob_selecao[genero] += recompensa / total_recompensa


decisao = Usuario(5)# intanciação

num_iteracoes = 100 

for _ in range(num_iteracoes):
    
    genero = random.choices(range(decisao.num_genero), weights=decisao.prob_selecao)[0]# interação do usuário
    recompensa = decisao.escolha_usuario(genero) #adiciona recompensa para o genero escolhido
    decisao.atualizar_probs(genero, recompensa)

generos_filmes = ["Ação", "Comédia", "Drama", "Ficção Científica", "Terror"] 

analisar_probabilidade = []

print("Probabilidades de escolha do perfil:")
for i, prob in enumerate(decisao.prob_selecao):
    analisar_probabilidade.append(prob)
    print(f"{generos_filmes[i]}: {prob}")
print("vetor retornado:", analisar_probabilidade)

def regra_de_tres(probabilidades, ate_cem_porcento):
    soma_atual = sum(probabilidades)
    probabilidades_normalizadas = [prob * ate_cem_porcento / soma_atual for prob in probabilidades]
    return probabilidades_normalizadas


probabilidades_finais = decisao.prob_selecao
ate_cem_porcento = 1.0

probabilidades_normalizadas = regra_de_tres(probabilidades_finais, ate_cem_porcento)

print("------------------------------")
print("Probabilidades em porcentagem:")
for i, prob in enumerate(probabilidades_normalizadas):
    prob_porcentagem = prob * 100
    analisar_probabilidade.append(prob_porcentagem)
    print(f"{generos_filmes[i]}: {prob_porcentagem:.2f}%")
    
print("------------------------------------------")


soma_valores = sum(probabilidades_normalizadas)
print("Soma dos valores:", soma_valores)