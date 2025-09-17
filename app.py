import pandas as pd
import streamlit as st
from unidecode import unidecode
import random

def normalizar_texto(texto: str) -> str:
    """Remove acentos e deixa em minúsculas"""
    return unidecode(texto.strip().lower())

def esconder_nome(nome: str, reveladas: set) -> str:
    """Esconde nome como na forca, revelando apenas letras selecionadas"""
    exibicao = ""
    for ch in nome:
        if ch == " ":
            exibicao += " "  # mantém espaços
        elif normalizar_texto(ch) in reveladas:
            exibicao += ch  # mostra letra revelada
        else:
            exibicao += "_"  # oculta
    return exibicao

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

        # Inicializar estados
        if "descobertos" not in st.session_state:
            st.session_state.descobertos = [None] * len(df_top5)
        if "dicas" not in st.session_state:
            st.session_state.dicas = [set() for _ in range(len(df_top5))]  # letras reveladas

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
            if st.session_state.descobertos[i]:
                nome_mostrado = row["Nome"]  # já descoberto
            else:
                # esconder nome com base nas letras já reveladas
                nome_mostrado = esconder_nome(row["Nome"], st.session_state.dicas[i])

            dica = f"Nacionalidade: {row['nationality']} | Posição: {row['Posicao']} | Gols: {row['goals']}"

            cols = st.columns([2, 1])  # layout: nome + botão
            with cols[0]:
                st.write(f"**{i+1}º posição** ({nome_mostrado})  →  {dica}")
            with cols[1]:
                if st.button(f"Dica {i+1}", key=f"dica-{i}"):
                    # Revela aleatoriamente uma letra do nome
                    letras_possiveis = [normalizar_texto(ch) for ch in row["Nome"] if ch.isalpha()]
                    if letras_possiveis:
                        letra_revelada = random.choice(letras_possiveis)
                        st.session_state.dicas[i].add(letra_revelada)

        # Finalização
        if all(st.session_state.descobertos):
            st.success("🎉 Parabéns! Você descobriu todos os jogadores!")
