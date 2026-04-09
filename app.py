import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import datetime

# --- CONFIGURAÇÕES DO APP ---
st.set_page_config(page_title="Café da Manhã - Estaleiro", page_icon="☕")

# Título visual
st.markdown("<h1 style='text-align: center; color: #5D4037;'>☕ Café da Manhã</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #795548;'>Estaleiro Guest House</h3>", unsafe_allow_html=True)
st.divider()

# --- 1. IDENTIFICAÇÃO BÁSICA ---
st.header("1. Sua Identificação")
col1, col2 = st.columns(2)
with col1:
    nome_hospede = st.text_input("Nome Completo", placeholder="Ex: João Silva")
    apto = st.text_input("Nº do Apartamento (APTO)", placeholder="Ex: 202")
with col2:
    data_servico = st.date_input("Data desejada", datetime.date.today() + datetime.timedelta(days=1))
    horario = st.time_input("Horário de entrega (08:30 às 11:00)", value=datetime.time(9, 0))
    local = st.selectbox("Local de entrega", ["Quarto", "Sacada da Suíte", "Sala da Casa", "Piscina", "Bistrô"])

st.divider()

# --- 2. O CARDÁPIO ---
st.header("2. Escolha seus itens")
pedido = []

# Função para adicionar item ao pedido
def adicionar_item(nome, qtd):
    pedido.append(f"{nome} ({qtd})")

# -- Seção: Pães e Básicos
st.subheader("🍞 Pães e Básicos")
c1, c2, c3 = st.columns(3)
with c1:
    if st.checkbox("Cesta de pães artesanais"):
        qtd = st.radio("Qtd (Cesta):", ["1 pax", "2 pax", "+"], key="p_art", horizontal=True)
        adicionar_item("Cesta pães artesanais", qtd)
with c2:
    if st.checkbox("Pães de queijo"):
        qtd = st.radio("Qtd (P.Queijo):", ["1 pax", "2 pax", "+"], key="p_qjo", horizontal=True)
        adicionar_item("Pães de queijo", qtd)
with c3:
    if st.checkbox("Bolo do dia"):
        adicionar_item("Bolo do dia", "Selecionado")

st.divider()

# -- Seção: Frios e Frutas
st.subheader("🧀 Frios, Frutas e Cereais")
c1, c2, c3 = st.columns(3)
with c1:
    if st.checkbox("Seleção de queijos"):
        adicionar_item("Seleção de queijos", "Selecionado")
    if st.checkbox("Seleção de defumados"):
        adicionar_item("Seleção de defumados", "Selecionado")
with c2:
    if st.checkbox("Frutas da estação"):
        qtd = st.radio("Qtd (Frutas):", ["1 pax", "2 pax", "+"], key="frut", horizontal=True)
        adicionar_item("Frutas da estação", qtd)
with c3:
    if st.checkbox("Granola"):
        qtd = st.radio("Qtd (Granola):", ["1 pax", "2 pax", "+"], key="grano", horizontal=True)
        adicionar_item("Granola", qtd)
    if st.checkbox("Iogurte Natural"):
        adicionar_item("Iogurte Natural", "Selecionado")

st.divider()

# -- Seção: Quentes (Ovos/Omeletes)
st.subheader("🍳 Pratos Quentes")
col_ovo1, col_ovo2 = st.columns(2)
with col_ovo1:
    if st.checkbox("Omelete"):
        adic_omelete = st.multiselect("Adicionais Omelete:", ["Queijo", "Presunto", "Tomate"])
        texto_omelete = f"Omelete (Adic: {', '.join(adic_omelete) if adic_omelete else 'Simples'})"
        qtd = st.radio("Qtd (Omelete):", ["1 pax", "2 pax"], key="oml", horizontal=True)
        adicionar_item(texto_omelete, qtd)
with col_ovo2:
    if st.checkbox("Ovos Mexidos"):
        qtd = st.radio("Qtd (Ovos):", ["1 pax", "2 pax"], key="ovos", horizontal=True)
        adicionar_item("Ovos Mexidos", qtd)

st.divider()

# -- Seção: Bebidas
st.subheader("☕ Bebidas")
bebidas_lista = ["Café Preto", "Café c/ Leite", "Leite Quente", "Chá Quente", "Suco Laranja natural", "Suco Uva integral", "Água Mineral"]
selecao_bebidas = st.multiselect("Selecione as bebidas:", bebidas_lista)
for b in selecao_bebidas:
    adicionar_item(b, "Selecionado")

st.divider()

# --- 3. OBSERVAÇÕES ---
st.header("3. Observações Finais")
obs = st.text_area("Restrições alimentares, alergias ou pedidos especiais:")

st.divider()

# --- FUNÇÃO PARA GERAR A IMAGEM ---
def gerar_imagem_comprovante(nome, apto, data, hora, local, itens, obs):
    # Criar uma imagem em branco (A4 proporcional, mas menor para mobile)
    largura, altura = 800, 1200
    # Tenta carregar um template, se não existir usa fundo branco
    try:
        img = Image.open("template.png").resize((largura, altura))
    except FileNotFoundError:
        img = Image.new('RGB', (largura, altura), color=(255, 255, 255))
    
    draw = ImageDraw.Draw(img)
    
    # Configurar Fontes (Streamlit Cloud usa fontes Linux padrão)
    try:
        font_titulo = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        font_itens = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        font_titulo = font_sub = font_itens = ImageFont.load_default()

    # Cores
    cor_texto = (60, 40, 30) # Marrom escuro

    # --- Desenhar Cabeçalho ---
    draw.text((largura//2, 50), "RESUMO DO PEDIDO", font=font_titulo, fill=cor_texto, anchor="ms")
    draw.text((largura//2, 90), "Café da Manhã - Estaleiro Guest House", font=font_sub, fill=cor_texto, anchor="ms")
    draw.line((50, 110, largura-50, 110), fill=cor_texto, width=2)

    # --- Dados do Hóspede ---
    y = 140
    draw.text((50, y), f"Hóspede: {nome}", font=font_sub, fill=cor_texto)
    draw.text((largura-250, y), f"APTO: {apto}", font=font_sub, fill=cor_texto)
    y += 40
    data_f = data.strftime('%d/%m/%Y')
    hora_f = hora.strftime('%H:%M')
    draw.text((50, y), f"Data: {data_f} | Hora: {hora_f} | Local: {local}", font=font_sub, fill=cor_texto)
    y += 50
    draw.line((50, y, largura-50, y), fill=cor_texto, width=1)
    y += 30

    # --- Lista de Itens ---
    draw.text((50, y), "ITENS SELECIONADOS:", font=font_sub, fill=cor_texto)
    y += 40
    for item in itens:
        draw.text((70, y), f"• {item}", font=font_itens, fill=cor_texto)
        y += 30
        if y > altura - 150: # Evitar quebrar a imagem
            break

    # --- Observações ---
    y += 40
    draw.line((50, y, largura-50, y), fill=cor_texto, width=1)
    y += 20
    draw.text((50, y), "OBSERVAÇÕES:", font=font_sub, fill=cor_texto)
    y += 35
    
    # Quebra de texto automática para obs
    import textwrap
    linhas_obs = textwrap.wrap(obs if obs else "Nenhuma.", width=60)
    for linha in linhas_obs:
        draw.text((70, y), linha, font=font_itens, fill=cor_texto)
        y += 25

    # Salvar em memória
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    return img_bytes.getvalue()


# --- BOTÃO DE FINALIZAR ---
st.divider()
if st.button("✅ GERAR MEU PEDIDO (IMAGEM)", type="primary"):
    if not nome_hospede or not apto or not pedido:
        st.error("⚠️ Por favor, preencha Nome, APTO e escolha pelo menos um item.")
    else:
        with st.spinner('Gerando imagem do pedido...'):
            img_data = gerar_imagem_comprovante(nome_hospede, apto, data_servico, horario, local, pedido, obs)
            
            # Mostra a imagem no app para o cliente ver
            st.image(img_data, caption="Seu pedido formatado")
            
            # Botão para baixar a imagem (necessário no mobile para depois anexar)
            st.download_button(
                label="📥 Baixar Imagem do Pedido",
                data=img_data,
                file_name=f"pedido_cafe_apto{apto}_{data_servico}.png",
                mime="image/png"
            )
            
            # Texto para o WhatsApp
            resumo_zap = f"Olá! Sou o hóspede *{nome_hospede}* do APTO *{apto}*.\nEstou enviando em anexo a imagem do meu pedido de café para amanhã, dia {data_servico.strftime('%d/%m')} às {horario.strftime('%H:%M')}."
            
            # --- AJUSTE SEU TELEFONE AQUI ---
            # Use formato: 55 + DDD + NUMERO (tudo junto, sem espaços)
            telefone_recepcao = "5547997957551" 
            
            link_zap = f"https://wa.me/{telefone_recepcao}?text={resumo_zap.replace(' ', '%20')}"
            
            st.warning("👉 Após baixar a imagem, clique no botão abaixo para abrir o WhatsApp da pousada e ANEXE a imagem que você acabou de baixar.")
            st.link_button("💬 Abrir WhatsApp e Anexar Imagem", link_zap)
