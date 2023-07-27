import streamlit as st
import pandas as pd
import numpy as np
import time
import random
import plotly.graph_objects as go



#--------------------------------------------MAB-----------------------------------------------------
class MultiArmedBandit:
    def __init__(self, num_bracos):
        self.num_bracos = num_bracos
        self.medias_recompensas = [1, 1, 1, 1, 1]  # Exemplo de recompensas personalizadas
        self.contagem_acoes = np.zeros(num_bracos)
        self.recompensas_cumulativas = np.zeros(num_bracos)


    def obter_recompensa(self, acao):
        peso_acao = peso_bracos[acao]
        recompensa = np.random.normal(self.medias_recompensas[acao], 0.1) * peso_acao
        self.contagem_acoes[acao] += 1
        self.recompensas_cumulativas[acao] += recompensa
        return recompensa



    def obter_melhor_braco(self):
        return np.argmax(self.medias_recompensas)

    def obter_acao_ucb(self, t):
        acoes = np.zeros(self.num_bracos)
        for i in range(self.num_bracos):
            if self.contagem_acoes[i] == 0:
                return i
            else:
                acoes[i] = (
                    self.recompensas_cumulativas[i] / self.contagem_acoes[i]
                    + np.sqrt(2 * np.log(t) / self.contagem_acoes[i])
                )
        return np.argmax(acoes)

    def obter_acao_aleatoria(self, pesos):
        probabilidades = pesos / np.sum(pesos)
        acao = np.random.choice(range(self.num_bracos), p=probabilidades)
        return acao
#---------------------------------------------PERFIL----------------------------------------------------------------    

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
    
    genero = random.choices(range(decisao.num_genero), weights=decisao.prob_selecao)[0] # interação do usuário
    recompensa = decisao.escolha_usuario(genero) #adiciona recompensa para o genero escolhido
    decisao.atualizar_probs(genero, recompensa)

generos_filmes = ["Ação", "Comédia", "Drama", "Ficção Científica", "Terror"] 

contexto_identificado = []

print("Probabilidades de escolha do perfil:")
for i, prob in enumerate(decisao.prob_selecao):
    contexto_identificado.append(prob)
    print(f"{generos_filmes[i]}: {prob}")
    
print("vetor retornado:", contexto_identificado)

def regra_de_tres(probabilidades, ate_cem_porcento):
    soma_atual = sum(probabilidades)
    probabilidades_normalizadas = [prob * ate_cem_porcento / soma_atual for prob in probabilidades]
    return probabilidades_normalizadas

#--------------------------------------------IMAGEM-----------------------------------------------------------


#--------------------------------------------------------------------------------------------------------
st.set_page_config(
    page_title="Contextual MAB",
    page_icon="🔫",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.snow()

st.title("Multi-Armed Bandits (MAB) Contextual")


st.sidebar.title("Configuração")
st.sidebar.selectbox('Selecione o MAB', ['Contextual'])

num_bracos = st.sidebar.number_input('Quantidade de braços', step=1, min_value=5, max_value=5)
num_passos = st.sidebar.slider('Quantidade de iterações', 0, 10000, 500)

if st.sidebar.button("Executar"):
    
    progress_text = "Processo🐙"
    my_bar = st.progress(0, text=progress_text)

    #col1, col2, col3 = st.columns(3)
    #col1.metric("Escolha principal", "🐙", f"{random.randint(9, 30)}%")
    #col2.metric("Pior escolha", "🔫", f"-{random.randint(0, 14)}%")
    #col3.metric("Assertividade UCB", "30%", "")

#--------------------------------USUARIO------------------------------------
    probabilidades_finais = decisao.prob_selecao
    ate_cem_porcento = 1.0

    probabilidades_normalizadas = regra_de_tres(probabilidades_finais, ate_cem_porcento)

    analisar_probabilidade = []
    tabela_dados = []

    for i, prob in enumerate(probabilidades_normalizadas):
        prob_porcentagem = prob * 100
        analisar_probabilidade.append(prob_porcentagem)
        tabela_dados.append({
            
            'Probabilidade de escolha': f"{prob_porcentagem:3.1f}%",
            'Generos': generos_filmes[i],
            })

    soma_valores = sum(probabilidades_normalizadas)
    tabela_dados = pd.DataFrame(tabela_dados[0:], columns=tabela_dados[0])
    tabela_dados_estilizada = tabela_dados.style.apply(lambda row: ['background-color: gray' if row['Probabilidade de escolha'] == tabela_dados['Probabilidade de escolha'].max() else '' for _ in row], axis=1)

    #st.subheader(f"Usuário {random.randint(16, 1000)}")
    #st.dataframe(tabela_dados_estilizada)
#-------
    labels = generos_filmes
    values = probabilidades_normalizadas
    max_value = max(values)
    fig = tabela_dados

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0 if v != max_value else 0.2 for v in values], hole=.5)])
    #st.write(fig)

    col1, col2 = st.columns([1, 2])

    col1.subheader(f"Usuário {random.randint(16, 1000)}")
    col1.dataframe(tabela_dados_estilizada)

    col2.subheader("")
    col2.write(fig)


#--------------------------------------------------------------------------

    

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)

    mab = MultiArmedBandit(num_bracos)

    recompensas = np.zeros(num_passos)
    contagem_acoes = np.zeros((num_passos, num_bracos))
    recompensas_cumulativas = np.zeros((num_passos, num_bracos))

    resultados_padrao = []

    peso_bracos = np.array(contexto_identificado)  # define a partir do contexto de cada perfil para que mostre ao usuario o genero (braço)
                                            # que ele mais curte pois quando um braço é escolhido o peso dele fica * a recompensa
    for t in range(num_passos):
        if np.random.uniform() < 0.1: # diminuir a taxa de UCB faz com que seja mostrado os variados tipos de generos ao usuário
            acao = mab.obter_acao_ucb(t + 1)
        else:
            acao = mab.obter_acao_aleatoria(peso_bracos)

        recompensa = mab.obter_recompensa(acao)

        recompensas[t] = recompensa
        contagem_acoes[t] = mab.contagem_acoes
        recompensas_cumulativas[t] = mab.recompensas_cumulativas

        # Salvar os resultados em sequência na lista
        resultados_padrao.append({
            'Iteração': t + 1,
            'Recompensa dos braços escolhidos': recompensa,
            'Contagem de escolhas por braço': mab.contagem_acoes.copy(),
            'Soma da recompensa por braço': mab.recompensas_cumulativas.copy()
        })

    melhor_braco = mab.obter_melhor_braco()
    recompensas_melhor_braco = recompensas_cumulativas[:, melhor_braco]

    chart_data = pd.DataFrame(recompensas_cumulativas, columns=[generos_filmes[i] for i in range(num_bracos)])

    st.subheader("Desempenho das ofertas (qual braço foi exibido)")
    st.line_chart(chart_data)

    chart_data_line = pd.DataFrame(recompensas_melhor_braco, columns=['Soma das recompenças'])

    df_resultados = pd.DataFrame(resultados_padrao)
    st.subheader("Tabela de Resultados")
    st.dataframe(df_resultados)