# Uaibot Paint Simulator

Este projeto permite gerar um tabuleiro de pintura a partir de uma imagem e simular um robô pintando os pixels usando Uaibot.

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

* Python 3.8+ (recomendado 3.10+)
* Git

E uma das seguintes IDEs/editores:

* VS Code
* PyCharm

---

## 🛠️ Instalação


1. **Crie um ambiente virtual** (recomendado)

   * **venv** (built‑in)

     ```bash
     python3 -m venv .venv
     source .venv/bin/activate   # Linux/macOS
     .venv\Scripts\activate     # Windows
     ```

   * **conda**

     ```bash
     conda create -n paint-sim python=3.10
     conda activate paint-sim
     ```

2. **Instale as dependências**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## 📂 Estrutura de Diretórios

```
uaibot-paint-simulator/
├── .streamlit/             # Configurações do Streamlit (opcional)
│   └── config.toml          # Configuração do Streamlit
├── .venv/                  # Ambiente virtual (opcional)
├── app.py
├── README.md
├── requirements.txt
└── src/
    ├── __init__.py
    ├── image_processing.py
    ├── board.py
    ├── robot_controller.py
    ├── interpolators.py
    ├── simulation.py
    └── streamlit_app.py
```

* **app.py**: ponto de entrada que chama `src/streamlit_app.py`.
* **requirements.txt**: lista de dependências (Streamlit, Uaibot, scikit-learn, Pillow, Matplotlib).
* **src/**: pacote principal com módulos organizados por responsabilidade.

---

## 🚀 Executando a Aplicação

1. **Ative** o ambiente virtual (se não estiver ativo):

   ```bash
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

2. **Execute** o Streamlit:

   ```bash
   streamlit run app.py
   ```

3. **Navegue** até o endereço exibido (por padrão: [http://localhost:8501](http://localhost:8501)).

4. **Use** o carregador de arquivos para enviar sua imagem (PNG/JPG/JPEG).

5. Ajuste o número de cores e resolução na barra lateral.

6. Clique em **Iniciar simulação** para ver o robô pintando.

# uaibot_paint-simulator
