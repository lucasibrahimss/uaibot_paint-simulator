import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(__file__))
from image_processing import ImageProcessor
from paint_simulation import run_simulation
from streamlit_utils import html_injection
import base64
os.system("pip install --upgrade --no-cache-dir git+https://github.com/rodrigo-arenas/uaibot.git")

def link_para_download_html(path_arquivo, nome_link="🔗 Abrir Simulação Interativa"):
    with open(path_arquivo, "rb") as f:
        conteudo = f.read()
    b64 = base64.b64encode(conteudo).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="simulacao.html">{nome_link}</a>'
    st.markdown(href, unsafe_allow_html=True)


def main():
    st.markdown(html_injection, unsafe_allow_html=True)
    st.set_page_config(
        page_title="Uaibot Paint Simulator",
        page_icon=":art:", layout="centered"
    )
    st.title("🎨 Uaibot Paint Simulator")
    st.markdown("Faça o upload de uma imagem para gerar o tabuleiro de pintura e simular o robô.")
    uploaded = st.file_uploader("Selecione uma imagem", type=['png','jpg','jpeg'])

    st.sidebar.header("Configurações")
    num_cores = st.sidebar.number_input("Número de cores", 2,10,6)
    n = st.sidebar.number_input("Resolução (n x n)", 2,36,16)

    if uploaded:
        with st.spinner("Processando imagem..."):
            proc = ImageProcessor(uploaded)
            proc.reduzir_cores(num_cores)
            proc.redimensionar(n,n)
            board_colors = proc.para_matriz_hex()

        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded, caption="Original")
        with col2:
            st.image(proc.imagem, caption="Reduzida")

        if st.button("Iniciar simulação"):
            with st.spinner("Executando..."):
                html_content=run_simulation(board_colors, n, n, num_cores)
                if html_content:
                    st.download_button(
                        label="⬇️ Baixar Simulação HTML",
                        data=html_content,
                        file_name="simulacao.html",
                        mime="text/html"
                )
                else:
                    st.error("Erro: conteúdo HTML da simulação não foi gerado.")


if __name__ == "__main__":
    main()
