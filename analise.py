import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


INPUT_FILE = "data/processed/spfc_jogos_tratados.csv"
OUTPUT_DIR_VISU = "data/visualizations"


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

def analisar_desempenho():

    print(f"Carregando dados tratados de: {INPUT_FILE}")
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {INPUT_FILE}")
        print("Certifique-se de que os scripts de coleta e transformação foram executados.")
        return

    print("Iniciando análise de desempenho...")

    
    df["resultado"] = df.apply(definir_resultado, axis=1)

    
    df["local_partida"] = df.apply(lambda row: "Casa" if row["time_casa"] == "Sao Paulo" else "Fora", axis=1)

  
    total_jogos = len(df)
    vitorias = df["resultado"].value_counts().get("Vitoria", 0)
    empates = df["resultado"].value_counts().get("Empate", 0)
    derrotas = df["resultado"].value_counts().get("Derrota", 0)
    
   
    desempenho_casa = df[df["local_partida"] == "Casa"]["resultado"].value_counts()
    desempenho_fora = df[df["local_partida"] == "Fora"]["resultado"].value_counts()

   
    print("\n--- ANÁLISE DE DESEMPENHO (Brasileirão 2023) ---")
    print(f"\nTotal de Jogos: {total_jogos}")
    print(f"Vitórias: {vitorias}")
    print(f"Empates: {empates}")
    print(f"Derrotas: {derrotas}")
    print(f"Aproveitamento: {((vitorias * 3 + empates) / (total_jogos * 3)) * 100:.2f}%")

    print(f"\n--- Desempenho em Casa ---")
    print(desempenho_casa.to_string())

    print("\n--- Desempenho Fora ---")
    print(desempenho_fora.to_string())
    
    
    OUTPUT_FILE_ANALISE = "data/results/spfc_analise_2023.csv"
    os.makedirs(os.path.dirname(OUTPUT_FILE_ANALISE), exist_ok=True)
    df.to_csv(OUTPUT_FILE_ANALISE, index=False, encoding="utf-8-sig")
    print(f"Análise salva em: {OUTPUT_FILE_ANALISE}")

    # Geração de gráficos
    os.makedirs(OUTPUT_DIR_VISU, exist_ok=True)

    plt.figure(figsize=(8, 6))
    sns.countplot(x="resultado",data=df, order=["Vitoria","Empate", "Derrota"], palette={"Vitoria": "green", "Empate":"gold", "Derrota":"red"})
    plt.title("Resultado do SPFC no Brasileirão 2023")
    plt.xlabel("Resultado")
    plt.ylabel("Número de Jogos")
    plt.savefig(os.path.join(OUTPUT_DIR_VISU, "resultado.png"))
    print(f"Gráfico \"resultado.png\" salvo em: {OUTPUT_DIR_VISU}")    
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.countplot(x="local_partida", hue="resultado", data=df, order=["Casa","Fora"],palette={"Vitoria": "green", "Empate": "gold", "Derrota": "red"})
    plt.title("Desempenho do SPFC jogando em casa e fora (Brasileirão 2023)")
    plt.xlabel("Local da Partida")
    plt.ylabel("Número de jogos")
    plt.legend(title="Resultado")
    plt.savefig(os.path.join(OUTPUT_DIR_VISU, "desempenho_casa_fora.png"))
    print(f"Gráfico \"desempenho_casa_fora.png\" salvo em: {OUTPUT_DIR_VISU}")
    plt.close()

    print("\nGeração de gráficos concluída.")

if __name__ == "__main__":
    analisar_desempenho()