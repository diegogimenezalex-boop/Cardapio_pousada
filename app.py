import streamlit as st

st.title("☕ Café da Manhã - Estaleiro Guest House")
st.subheader("Personalize seu pedido")

# 1. Identificação Básica
nome_hospede = st.text_input("Nome do Hóspede")
apto = st.text_input("Nº do Apartamento (APTO)")

col1, col2 = st.columns(2)
with col1:
    horario = st.time_input("Horário para ser servido (08:30 às 11:00)")
with col2:
    local = st.selectbox("Local", ["Quarto", "Sacada da Suíte", "Sala da Casa", "Piscina", "Bistrô"])

st.divider()

# 2. Itens do Cardápio
st.header("🛒 Escolha os itens")

itens_selecionados = {}

# Exemplo de Seção: Pães e Comidas
opcoes_comida = ["Cesta de pães artesanais", "Pães de queijo", "Seleção de queijos fatiados", 
                 "Seleção de defumados fatiados", "Frutas da estação", "Bolo do dia"]

for item in opcoes_comida:
    check = st.checkbox(item)
    if check:
        qtd = st.radio(f"Quantidade para {item}:", ["1 pax", "2 pax", "ou +"], horizontal=True)
        itens_selecionados[item] = qtd

st.divider()

# 3. Ovos e Especiais
if st.checkbox("Omelete (Ovos, manteiga, leite e sal)"):
    adic = st.multiselect("Adicionais Omelete:", ["Queijo", "Presunto", "Cubos de tomates frescos"])
    itens_selecionados["Omelete"] = f"Adicionais: {', '.join(adic)}"

# 4. Bebidas e Adicionais
st.header("☕ Bebidas")
bebidas = ["Café", "Leite quente", "Chá", "Suco de Laranja", "Suco de Uva", "Água Mineral", "Iogurte Natural"]
for b in bebidas:
    if st.checkbox(b):
        itens_selecionados[b] = "Selecionado"

# 5. Observações
obs = st.text_area("Observações/Adicionais")

# Botão de Envio
if st.button("Finalizar Pedido"):
    resumo = f"*Pedido de Café - APTO {apto}*\n"
    resumo += f"Hóspede: {nome_hospede}\n"
    resumo += f"Horário: {horario} | Local: {local}\n\n"
    for k, v in itens_selecionados.items():
        resumo += f"- {k}: {v}\n"
    resumo += f"\n*Obs:* {obs}"
    
    # Link direto para o WhatsApp da Pousada
    telefone_pousada = "5547999999999" # Substitua pelo seu
    link_zap = f"https://wa.me/{telefone_pousada}?text={resumo.replace(' ', '%20')}"
    
    st.success("Pedido gerado com sucesso!")
    st.write(resumo)
    st.link_button("Enviar para o WhatsApp da Recepção", link_zap)
