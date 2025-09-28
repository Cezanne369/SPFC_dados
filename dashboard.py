import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Dashboard SPFC - Brasileirão 2023",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para definir resultado
def definir_resultado(row):
    if row["time_casa"] == "Sao Paulo":
        if row["gols_casa"] > row["gols_fora"]:
            return "Vitoria"
        elif row["gols_casa"] < row["gols_fora"]:
            return "Derrota"
        else:
            return "Empate"
    else:
        if row["gols_fora"] > row["gols_casa"]:
            return "Vitoria"
        elif row["gols_fora"] < row["gols_casa"]:
            return "Derrota"
        else:
            return "Empate"

# Função para carregar dados
@st.cache_data
def carregar_dados():
    try:
        # Primeiro tenta carregar o arquivo tratado
        df = pd.read_csv("data/processed/spfc_jogos_tratados.csv")
        
        # Adiciona colunas de análise
        df["resultado"] = df.apply(definir_resultado, axis=1)
        df["local_partida"] = df.apply(lambda row: "Casa" if row["time_casa"] == "Sao Paulo" else "Fora", axis=1)
        
        return df
    except FileNotFoundError:
        st.error(" Arquivo de dados não encontrado. Execute primeiro os scripts de coleta e transformação.")
        return None

# Função para calcular estatísticas
def calcular_estatisticas(df):
    total_jogos = len(df)
    vitorias = df["resultado"].value_counts().get("Vitoria", 0)
    empates = df["resultado"].value_counts().get("Empate", 0)
    derrotas = df["resultado"].value_counts().get("Derrota", 0)
    aproveitamento = ((vitorias * 3 + empates) / (total_jogos * 3)) * 100
    
    return {
        "total_jogos": total_jogos,
        "vitorias": vitorias,
        "empates": empates,
        "derrotas": derrotas,
        "aproveitamento": aproveitamento
}

# Função para criar gráfico de resultados
def criar_grafico_resultados(df):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.countplot(
        x="resultado", 
        data=df, 
        order=["Vitoria", "Empate", "Derrota"], 
        palette={"Vitoria": "green", "Empate": "gold", "Derrota": "red"},
        ax=ax
    )
    ax.set_title("Resultados do SPFC no Brasileirão 2023", fontsize=16, fontweight="bold")
    ax.set_xlabel("Resultado", fontsize=12)
    ax.set_ylabel("Número de Jogos", fontsize=12)
    
    # Adiciona valores nas barras
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                   (p.get_x() + p.get_width()/2., p.get_height()), 
                   ha='center', va='bottom', fontsize=12, fontweight="bold")
    
    plt.tight_layout()
    return fig

# Função para criar gráfico casa vs fora
def criar_grafico_casa_fora(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(
        x="local_partida", 
        hue="resultado", 
        data=df, 
        order=["Casa", "Fora"],
        palette={"Vitoria": "green", "Empate": "gold", "Derrota": "red"},
        ax=ax
    )
    ax.set_title("Desempenho do SPFC em Casa vs Fora - Brasileirão 2023", fontsize=16, fontweight="bold")
    ax.set_xlabel("Local da Partida", fontsize=12)
    ax.set_ylabel("Número de Jogos", fontsize=12)
    ax.legend(title="Resultado", title_fontsize=12, fontsize=10)
    
    # Adiciona valores nas barras
    for p in ax.patches:
        if p.get_height() > 0:
            ax.annotate(f'{int(p.get_height())}', 
                       (p.get_x() + p.get_width()/2., p.get_height()), 
                       ha='center', va='bottom', fontsize=10, fontweight="bold")
    
    plt.tight_layout()
    return fig

# Interface principal
def main():
    # Título principal
    st.title("Dashboard SPFC - Brasileirão 2023")
    st.markdown("---")
    
    # Carrega os dados
    df = carregar_dados()
    
    if df is not None:
        # Sidebar com filtros
        st.sidebar.header("Filtros")
        
        # Filtro por local da partida
        local_opcoes = ["Todos"] + list(df["local_partida"].unique())
        local_selecionado = st.sidebar.selectbox("Local da Partida:", local_opcoes)
        
        # Filtro por resultado
        resultado_opcoes = ["Todos"] + list(df["resultado"].unique())
        resultado_selecionado = st.sidebar.selectbox("Resultado:", resultado_opcoes)
        
        # Aplica filtros
        df_filtrado = df.copy()
        if local_selecionado != "Todos":
            df_filtrado = df_filtrado[df_filtrado["local_partida"] == local_selecionado]
        if resultado_selecionado != "Todos":
            df_filtrado = df_filtrado[df_filtrado["resultado"] == resultado_selecionado]
        
        # Estatísticas principais
        stats = calcular_estatisticas(df_filtrado)
        
        st.header("Estatísticas Principais")
        
        # Métricas em colunas
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total de Jogos", stats["total_jogos"])
        with col2:
            st.metric("Vitórias", stats["vitorias"])
        with col3:
            st.metric("Empates", stats["empates"])
        with col4:
            st.metric("Derrotas", stats["derrotas"])
        with col5:
            st.metric("Aproveitamento", f"{stats["aproveitamento"]:.1f}%")
        
        st.markdown("---")
        
        # Gráficos
        st.header("Visualizações")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribuição de Resultados")
            if len(df_filtrado) > 0:
                fig1 = criar_grafico_resultados(df_filtrado)
                st.pyplot(fig1)
            else:
                st.warning("Nenhum dado encontrado para os filtros selecionados.")
        
        with col2:
            st.subheader("Desempenho Casa vs Fora")
            if len(df_filtrado) > 0 and local_selecionado == "Todos":
                fig2 = criar_grafico_casa_fora(df_filtrado)
                st.pyplot(fig2)
            elif local_selecionado != "Todos":
                st.info("Gráfico disponível apenas quando 'Todos' os locais estão selecionados.")
            else:
                st.warning("Nenhum dado encontrado para os filtros selecionados.")
        
        st.markdown("---")
        
        # Tabela de dados
        st.header("Dados Detalhados")
        
        if len(df_filtrado) > 0:
            # Seleciona colunas relevantes para exibição
            colunas_exibir = ["data_partida", "time_casa", "gols_casa", "gols_fora", "time_fora", "resultado", "local_partida"]
            df_exibir = df_filtrado[colunas_exibir].copy()
            
            # Renomeia colunas para melhor visualização
            df_exibir.columns = ["Data", "Time Casa", "Gols Casa", "Gols Fora", "Time Fora", "Resultado", "Local"]
            
            st.dataframe(df_exibir, use_container_width=True)
            
            # Botão para download
            csv = df_exibir.to_csv(index=False)
            st.download_button(
                label="Baixar dados filtrados (CSV)",
                data=csv,
                file_name=f"spfc_dados_filtrados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("Nenhum dado encontrado para os filtros selecionados.")
        
        # Informações adicionais
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Sobre")
        st.sidebar.markdown("Dashboard interativo para análise do desempenho do São Paulo FC no Brasileirão 2023.")
        st.sidebar.markdown("**Dados:** Jogos do campeonato brasileiro")
        st.sidebar.markdown("**Última atualização:** " + datetime.now().strftime("%d/%m/%Y %H:%M"))

if __name__ == "__main__":
    main()