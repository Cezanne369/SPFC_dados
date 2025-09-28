# 🟥⬜⬛ SPFC Dados

📊 Dados, estatísticas e um pouco de **paixão tricolor** no mundo da tecnologia!  
Esse projeto nasceu para treinar **engenharia de dados** na prática, mas acabou virando uma forma de unir duas coisas que curto bastante: **Python** e **futebol** ⚽🔥.

---

## 🎯 O que esse projeto faz?

- **Coleta de dados**: scripts que puxam informações automaticamente.  
- **Transformação**: limpeza, padronização e preparação dos dados para análise.  
- **Armazenamento**: dados salvos em formatos rápidos e eficientes como **Parquet** e **CSV**.  
- **Dashboard**: visualização interativa dos dados com **Streamlit**.  
- **Automação**: pipeline organizado em etapas (coleta → transformação → organização → visualização).  

---

## 🧩 Estrutura do projeto

📂 **SPFC_dados/**  
├── `api.py` → responsável por puxar dados via API  
├── `coleta.py` → coleta de dados brutos  
├── `transformação.py` → limpeza e padronização dos dados  
├── `organização.py` → organiza os dados e exporta para CSV/Parquet  
├── `dashboard.py` → interface interativa para análise (Streamlit)  
├── `main.py` → orquestração do pipeline  
├── `data/` → pasta onde os dados ficam salvos  
├── `README.md` → você está aqui 😉  

---

## 🚀 Como rodar na sua máquina

1. Clone o repositório:
   ```bash
   git clone https://github.com/Cezanne369/SPFC_dados.git
   cd SPFC_dados
   ```

2. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate    # Windows
   source venv/bin/activate # Linux/Mac
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o pipeline:
   ```bash
   python main.py
   ```

5. Abra o dashboard:
   ```bash
   streamlit run dashboard.py
   ```

---

## 🛠️ Tecnologias utilizadas

- **Python 3.10+**  
- **Pandas** (manipulação de dados)  
- **PyArrow / Fastparquet** (formato Parquet)  
- **Requests** (coleta de dados via API)  
- **Streamlit** (dashboard interativo)  
- **Git & GitHub** (versionamento)  

---

## 📊 Exemplos de resultados

- Dados históricos organizados em tabelas 🔢  
- Visualizações sobre desempenho, estatísticas e análises ⚽  
- Arquivos `.csv` e `.parquet` prontos para serem consumidos em outras ferramentas  

*(spoiler: em breve, gráficos mais estilosos e insights automáticos 😏)*

---

## 🤝 Como contribuir

Se você também curte dados + futebol, sinta-se à vontade para contribuir:  

1. Faça um fork do projeto  
2. Crie uma branch (`git checkout -b minha-feature`)  
3. Commit suas mudanças (`git commit -m "adicionei uma nova feature"`)  
4. Faça o push (`git push origin minha-feature`)  
5. Abra um Pull Request 🚀  

---

## 👨‍💻 Autor

Feito por **Jean Paul Cézanne Silva Borja**  
📧 Email: *jeanpcezanne@gmail.com*  
🔗 LinkedIn: *www.linkedin.com/in/jean-paul-cézanne*  

---

> "Futebol é paixão. Dados são precisão. Aqui os dois se encontram." 🟥⬜⬛
