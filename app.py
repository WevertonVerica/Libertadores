import pandas as pd
import streamlit as st
from unidecode import unidecode  # <- precisa estar no requirements.txt

def normalizar_texto(texto: str) -> str:
    """Remove acentos e deixa em minúsculas"""
    return unidecode(texto.strip().lower())

# =======================
# Streamlit App
# =======================
st.title("Jogo dos Artilheiros da Libertadores ⚽")

# Carregar dados
df = pd.read_csv("artilheiroslibertadores.csv")

# Input do usuário
letra = st.text_input("Escolha uma letra para adivinhar os artilheiros:").strip().upper()

if letra:
    # Filtra top 5 por letra
    df_filtrado = df[df["Nome"].str.upper().str.startswith(letra)]
    df_top5 = df_filtrado.sort_values(by="goals", ascending=False).head(5).reset_index(drop=True)
    
    if df_top5.empty:
        st.warning("Nenhum jogador encontrado com essa letra.")
    else:
        st.write("Tente adivinhar os 5 maiores artilheiros com essa letra!")
        
        # Criar campos de input para cada jogador
        respostas = []
        for i, row in df_top5.iterrows():
            st.write(f"Dica {i+1}: Nacionalidade: {row['nationality']}, Posição: {row['Posicao']}, Gols: {row['goals']}")
            tentativa = st.text_input(f"Quem é o jogador {i+1}?", key=i)
            respostas.append((tentativa, row['Nome']))
        
        # Botão para checar respostas
        if st.button("Verificar respostas"):
            pontos = 0
            for tentativa, correto in respostas:
                tentativa_norm = normalizar_texto(tentativa)
                correto_norm = normalizar_texto(correto)
                
                # regra 1: acerto total (sem acentos, case insensitive)
                if tentativa_norm == correto_norm:
                    pontos += 1
                else:
                    # regra 2: acerto parcial (qualquer parte do nome)
                    partes = correto_norm.split()
                    if any(p in tentativa_norm for p in partes):
                        pontos += 1

            st.success(f"Você acertou {pontos} de 5!")
