# pip install streamlit
# pip install streamlit_option_menu

import streamlit as st
import pandas as pd
import plotly.express as px
from  streamlit_option_menu import  option_menu
from query import conexao

# *** PRIMEIRA CONSULTA / ATUALIZACOES DE DADOS ***
# Consultar os dados
query = "SELECT * FROM tb_carro"


# Carregar os dados
df = conexao(query)


# Botao para atualizar
if st.button("Atualizar Dados"):
    df = conexao(query)


# ****** ESTRUTURA LATERA DE FILTROS ******
st.sidebar.header("Selecione o Filtro")

marca = st.sidebar.multiselect("Marca Selecionada", # Nome do seletor
                               options=df["marca"].unique(), # opcoes disponiveis
                               default=df["marca"].unique() # as Marcas
                               )

modelo = st.sidebar.multiselect("Modelo Selecionado",
                                options=df["modelo"].unique(),
                                default=df["modelo"].unique()
                                )

ano = st.sidebar.multiselect("Ano Selecionado",
                            options=df["ano"].unique(),
                            default=df["ano"].unique()
                                )

valor = st.sidebar.multiselect("valor Selecionado",
                               options=df["valor"].unique(),
                               default=df["valor"].unique()
                               )

cor = st.sidebar.multiselect("cor Selecionada",
                             options=df["cor"].unique(),
                             default=df["cor"].unique()
                             )

numero_vendas = st.sidebar.multiselect("numero de vendas",
                                       options=df["numero_vendas"].unique(),
                                       default=df["numero_vendas"].unique()
                                       )

# Aplicar os filtros selecionados

df_selecionado = df[
    (df["marca"].isin(marca)) &
    (df["modelo"].isin(modelo)) &
    (df["ano"].isin(ano)) &
    (df["valor"].isin(valor)) &
    (df["cor"].isin(cor)) &
    (df["numero_vendas"].isin(numero_vendas)) 
]


# ***** EXIBIR VALORES MEDIOS - ESTATISTICA *****

def Home():
    with st.expander("Tabela"): # Cria uma caix aexpansivel com um titulo
        mostrarDados = st.multiselect('Filter: ', df_selecionado.columns, default=[])

        # Verifica se o usuario selecionou colunas para exibir
        if mostrarDados:
            # Exibe os dados filtrados pelas colunas selecionadas
            st.write(df_selecionado[mostrarDados])
    # Verifica se o Dataframe filtrado (df_selecionado) nao esta vazio
    if not df_selecionado.empty:   
        venda_total = df_selecionado["numero_vendas"].sum()  
        venda_media = df_selecionado["numero_vendas"].mean()        
        venda_mediana = df_selecionado["numero_vendas"].median() 


        total1, total2, total3 = st.columns(3, gap="large")

        with total1:
            st.info("Valor Total de Vendas dos Carros", icon='📌')
            st.metric(label="Total", value=f"{venda_total:,.0f}")

        with total2:
            st.info("Valor Medio das Vendas", icon='📌')    
            st.metric(label="Media", value=f"{venda_media:,.0f}")

        with total3:
            st.info("Valor Mediano dos Carros", icon='📌')    
            st.metric(label="Mediana", value=f"{venda_mediana:,.0f}")

    # Exibe um aviso se nao houver dados disponiveis com os filtros aplicados
    else:
        st.warning("Nenhum dado disponivel com os filtros selecionados")
    # Insere uma linha divisoria para separar as secoes
    st.markdown(""" ----------""")  


    # *************** GRAFICOS ***************

def graficos(df_selecionado):
        # Verifica se o dataframe filtrado esta vazio. Se estiver vazio, exibe uma mensagem
        # que nao ha dados disponiveis para gerar graficos e interrompe a execucao da funcao
    if df_selecionado.empty:
        st.warning("Nenhum dado disponivel para gerar graficos")
        # interrompe a funcao, pq nao ha motivo para continuar executando se nao tem dados
        return

    # Criacáo dos graficos
    # 4 abas -> Graficos de Barras, Graficos de linhas, Grafico de Pizza e Dispersao

    graf1, graf2, graf3, graf4, graf5 = st.tabs(["Grafico de Barras", "Grafico de Linhas", "Grafico de Pizza", "Grafico de Dispersao","Grafico de Area"])

    with graf1:
        st.write("Grafico de Barras") # Titulo

        # Agrupa pela marca e conta o numero de ocorrencias da coluna valor. Depois ordena o resultado de forma decrescente
        investimento = df_selecionado.groupby("marca").count()[["valor"]].sort_values(by="valor", ascending=False)

        fig_valores = px.bar(investimento,  # Dataframe qeu contem os dados sobres valores por marca
                                x=investimento.index, 
                                y="valor",
                                orientation="h",
                                title="<b>Valores de Carros</b>",
                                color_discrete_sequence=["#0083b3"])

        # Exibe a figura e ajusta a tela para ocupar toda a largura disponivel.
        st.plotly_chart(fig_valores, use_container_width=True)


    with graf2:
        st.write("Grafico de Linhas")
        dados = df_selecionado.groupby("marca").count()[["valor"]]

        fig_valores2 = px.line(dados, 
                                x=dados.index,
                                y="valor",
                                title="<b>Valores por Marca</b>",
                                color_discrete_sequence=["#0083b3"])
        
        st.plotly_chart(fig_valores2, use_container_width=True)

    with graf3:
        st.write("Grafico de Pizza")
        dados2 = df_selecionado.groupby("marca").sum()[["valor"]]
        
        fig_valores3 = px.pie(dados2,
                                values="valor", # Valores que serao representados
                                names=dados2.index,# Os nomes (marcas) que irao rotular
                                title="<b>Distribuicao de Valores por Marca</b>")


        st.plotly_chart(fig_valores3, use_container_width=True)
        

    with graf4:
        st.write("Grafico de Dispersao")   
        dados3 = df_selecionado.melt(id_vars=["marca"], value_vars=["valor"])
        
        fig_valores4 = px.scatter(dados3,
                                    x="marca",
                                    y="value",
                                    color="variable",
                                    title="<b>Dispersao de valores por marca</b>")

        st.plotly_chart(fig_valores4, use_container_width=True)

 
    # Criado por Bruno
  
    with graf5:
        st.write("Gráfico de Área")
        dados4 = df_selecionado.groupby("marca").count()[["valor"]].sort_values(by="valor", ascending=False).reset_index()

        fig_valores5 = px.area(dados4, x="marca", y="valor", title="Distribuição de Valores por Marca",
                  labels={"marca": "Marca", "valor": "Quantidade de Valores"})

   
        st.plotly_chart(fig_valores5, use_container_width=True)
   
     

# *********  Barra de Progresso ***************      

def barraprogresso():
    valorAtual = df_selecionado["numero_vendas"].sum()
    objetivo = 2000000
    percentual = round((valorAtual/objetivo * 100))
    

    if percentual > 100:
        st.subheader("Valores Atingidos!!!")

    else:
        st.write(f"Voce tem {percentual}% de {objetivo}. Corra atras filhao!!") 

        mybar = st.progress(0)
        for percentualCompleto in range(percentual):
            mybar.progress(percentualCompleto +1, text="Alvo %")
# *********************** MENU LATERAL *******************            

def menuLateral():
    with st.sidebar:
        selecionado = option_menu(menu_title="Menu", options=["Home", "Progresso"], 
        icons=["house","eye"], menu_icon="cast",
        default_index=0)

    if selecionado == "Home":
        st.subheader(f"Pagina: {selecionado}")
        Home()
        graficos(df_selecionado)

    if selecionado == "Progresso":
        st.subheader(f"Pagina: {selecionado}")
        barraprogresso()
        graficos(df_selecionado)

# ******* Ajustar o CSS ************


menuLateral()








         