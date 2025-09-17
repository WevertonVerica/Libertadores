import pandas as pd
import streamlit as st

# =======================
# Streamlit App
# =======================
st.title("Jogo dos Artilheiros da Libertadores ⚽")

# Carregar dados
df = pd.read_csv("artilheiroslibertadores.csv")  # seu CSV pronto

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
                if tentativa.strip().lower() == correto.lower():
                    pontos += 1
            st.success(f"Você acertou {pontos} de 5!")
