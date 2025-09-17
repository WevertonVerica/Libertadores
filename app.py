import pandas as pd
import streamlit as st
from unidecode import unidecode

def normalizar_texto(texto: str) -> str:
    """Remove acentos e deixa em minúsculas"""
    return unidecode(texto.strip().lower())

# =======================
# Streamlit App
# =======================
st.title("Jogo dos Artilheiros da Libertadores ⚽")

# Carregar dados
df = pd.read_csv("artilheiroslibertadores.csv")

# Input da letra inicial
letra = st.text_input("Escolha uma letra para começar:").strip().upper()

if letra:
    # Filtra top 5 por letra
    df_filtrado = df[df["Nome"].str.upper().str.startswith(letra)]
    df_top5 = df_filtrado.sort_values(by="goals", ascending=False).head(5).reset_index(drop=True)
    
    if df_top5.empty:
        st.warning("Nenhum jogador encontrado com essa letra.")
    else:
        st.write("Tente adivinhar os 5 maiores artilheiros com essa letra!")

        # Inicializar estado de jogadores descobertos
        if "descobertos" not in st.session_state:
            st.session_state.descobertos = [None] * len(df_top5)

        # Campo único para chute
        chute = st.text_input("Digite o nome de um jogador:")

        if st.button("Chutar"):
            chute_norm = normalizar_texto(chute)
            for i, row in df_top5.iterrows():
                if st.session_state.descobertos[i] is None:
                    correto_norm = normalizar_texto(row["Nome"])
                    partes = correto_norm.split()
                    
                    # acerto total ou parcial
                    if chute_norm == correto_norm or any(p in chute_norm for p in partes):
                        st.session_state.descobertos[i] = row["Nome"]

        # Mostrar tabela de posições + dicas
        st.write("---")
        for i, row in df_top5.iterrows():
            nome_mostrado = st.session_state.descobertos[i] if st.session_state.descobertos[i] else "______________________"
            dica = f"Nacionalidade: {row['nationality']} | Posição: {row['Posicao']} | Gols: {row['goals']}"
            st.write(f"**{i+1}º posição** ({nome_mostrado})  →  {dica}")

        # Finalização
        if all(st.session_state.descobertos):
            st.success("🎉 Parabéns! Você descobriu todos os jogadores!")
