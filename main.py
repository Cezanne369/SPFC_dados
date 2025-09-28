import subprocess
import os
import sys

def run_script(script_name, working_dir, check=True):
    print(f"\n--- Executando {script_name} ---")
    try:
        result = subprocess.run([sys.executable, script_name], cwd=working_dir, capture_output=True, text=True, check=check)
        print(result.stdout)
        if result.stderr:
            print(f"Erros/Warnings de {script_name}:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar {script_name}:\n{e.stdout}\n{e.stderr}")
        print("Abortando a execução.")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Erro: O script {script_name} não foi encontrado em {working_dir}.")
        print("Abortando a execução.")
        sys.exit(1)

def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Coleta de Dados
    run_script("coleta.py", project_dir)
    
    # 2. Transformação de Dados
    run_script("transformação.py", project_dir)
    
    # 3. Análise de Dados e Geração de Gráficos Estáticos
    run_script("analise.py", project_dir)
    
    print("\n--- Pipeline de dados concluído! ---")
    print("\n--- Iniciando o Dashboard Streamlit ---")
    print("Isso abrirá o dashboard no seu navegador web. Pressione Ctrl+C no terminal para parar o dashboard.")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"], cwd=project_dir, check=False)
    except FileNotFoundError:
        print("Erro: Streamlit não encontrado. Certifique-se de que está instalado (pip install streamlit).")
        sys.exit(1)

if __name__ == "__main__":
    main()