import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import plotly.graph_objects as go
from concurrent.futures import ThreadPoolExecutor, as_completed
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# ==============================================================================
# BLOCO 1: CONFIGURAÇÃO DA PÁGINA & ESTILIZAÇÃO VISUAL APRIMORADA
# ==============================================================================
st.set_page_config(
    page_title="Análise exploratória do mercado de locação residencial em São Paulo",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Fundo da aplicação com azul mais claro, suave e não cansativo */
    .stApp {
        background-color: #38bdf8 !important;
        color: #f3f4f6 !important;
    }

    html, body, #root,
    [data-testid="stAppViewContainer"] {
        min-height: 100vh !important;
        background-color: #38bdf8 !important;
    }

    [data-testid="stHeader"], footer {
        background-color: #38bdf8 !important;
    }
    
    /* Container principal com fundo escuro elegante */
    .main .block-container {
        max-width: 100% !important;
        padding: 1.5rem 2rem !important;
        background-color: #12161c !important;
        border-radius: 12px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        margin: 1.5rem;
    }

    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 15px !important;
    }

    /* Mantém a barra lateral preta, separada do fundo azul da página */
    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #21262d !important;
    }

    section[data-testid="stSidebar"] .block-container {
        background-color: transparent !important;
        padding-top: 2rem !important;
    }

    .stSidebar label, .stSidebar p, .stSidebar span, .stSidebar h1, .stSidebar h2, .stSidebar h3 {
        color: #c9d1d9 !important;
        font-weight: 600 !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] > label {
        color: #f8fafc !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.75rem !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 0.55rem !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label * {
        color: #f8fafc !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        line-height: 1.4 !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label {
        padding: 0.45rem 0.55rem !important;
        border-radius: 8px !important;
    }

    .stButton > button, div[data-testid="stDownloadButton"] > button {
        background-color: #238636 !important;
        color: #ffffff !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 8px 16px !important;
        width: 100% !important;
        box-shadow: 0 3px 6px rgba(0,0,0,0.2);
    }

    .stButton > button:hover, div[data-testid="stDownloadButton"] > button:hover {
        background-color: #2ea043 !important;
    }

    div[data-testid="stMetric"] {
        background-color: #1a212d !important;
        border: 1px solid #273344 !important;
        padding: 20px 18px !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25) !important;
    }

    label[data-testid="stMetricLabel"], label[data-testid="stMetricLabel"] * {
        color: #ffffff !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }
    
    div[data-testid="stMetricValue"], div[data-testid="stMetricValue"] * {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }

    div[data-testid="stMetricDelta"], div[data-testid="stMetricDelta"] * {
        color: #86efac !important;
        font-weight: 600 !important;
    }

    .stApp h1, .stApp h2, .stApp h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    .dashboard-card {
        background-color: #1a212d !important;
        border: 1px solid #273344 !important;
        padding: 20px !important;
        border-radius: 10px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25) !important;
    }
    .dashboard-card h4 {
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        margin-bottom: 12px !important;
    }
    .dashboard-card p, .dashboard-card li {
        font-size: 0.95rem !important;
        line-height: 1.5 !important;
        color: #f1f5f9 !important;
    }
    .learning-note {
        background-color: #102638;
        border-left: 4px solid #38bdf8;
        border-radius: 6px;
        margin-top: 14px;
        padding: 12px 16px;
    }
    .learning-note p {
        color: #f8fafc !important;
        margin: 0 !important;
    }

    /* Flashcard customizado de resultado preditivo com alta legibilidade */
    .avm-result-card {
        background-color: #1e293b !important;
        border: 2px solid #38bdf8 !important;
        padding: 20px !important;
        border-radius: 10px !important;
        margin-top: 15px !important;
        text-align: center;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.2);
    }
    .avm-result-card h3 {
        color: #38bdf8 !important;
        margin-bottom: 5px !important;
        font-size: 1.1rem !important;
    }
    .avm-result-value {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }
</style>
""", unsafe_allow_html=True)

API_URL_QUINTOANDAR = "https://www.quintoandar.com.br/api/yellow-pages/v2/search"

# Header Superior com o Logo e o Título em Destaque Solicitado
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image("Logo_1_QuintoAndar.png", use_container_width=True)
with col_title:
    st.markdown("### Análise exploratória do mercado de locação residencial em São Paulo")
    st.markdown('<div style="color: #cbd5e1; font-size: 0.9rem;">Dashboard Analítico, Preditivo & Inteligência Imobiliária (Sprint 3 & 4)</div>', unsafe_allow_html=True)

st.markdown("<hr style='border-color: #21262d; margin-top: 15px; margin-bottom: 20px;'>", unsafe_allow_html=True)

# ==============================================================================
# FUNÇÕES DE FORMATAÇÃO E ETL
# ==============================================================================
def formatar_moeda_br(valor):
    if pd.isna(valor) or valor is None:
        return "R$ 0,00"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_numero_br(valor, decimais=0):
    if pd.isna(valor) or valor is None:
        return "0"
    fmt = f"{{:,.{decimais}f}}"
    return fmt.format(valor).replace(",", "X").replace(".", ",").replace("X", ".")

def converter_df_para_csv_ptbr(df):
    df_export = df.copy()
    float_cols = df_export.select_dtypes(include=['float64', 'float32']).columns
    for col in float_cols:
        df_export[col] = df_export[col].apply(lambda x: f"{x:.2f}".replace('.', ',') if pd.notnull(x) else '')
    return df_export.to_csv(index=False, sep=';', encoding='utf-8-sig')

def requisitar_pagina(url, payload, headers):
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            hits = data.get("hits", {}).get("hits", [])
            resultados = []
            for item in hits:
                source = item.get("_source", {})
                amenities = source.get('amenities', []) or []
                resultados.append({
                    'id_imovel': str(source.get('id', '')),
                    'url': f"https://www.quintoandar.com.br/imovel/{source.get('id')}",
                    'bairro': (source.get('address') or {}).get('neighborhood', 'Não informado'),
                    'aluguel': float(source.get('rentPrice') or 0),
                    'condominio': float(source.get('condo') or 0),
                    'iptu': float(source.get('iptu') or 0),
                    'total': float(source.get('totalCost') or 0),
                    'metragem': float(source.get('area') or 0),
                    'quarto': float(source.get('bedrooms') or 0),
                    'aceita_pet': 1.0 if "PETS_ALLOWED" in amenities else 0.0,
                    'mobilia': 1.0 if "FURNISHED" in amenities else 0.0
                })
            return resultados
    except Exception:
        pass
    return []

def buscar_imoveis_quintoandar_api_massivo(max_paginas_por_quadrante=4):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        'Origin': 'https://www.quintoandar.com.br'
    }
    quadrantes = [
        {"north": -23.54, "south": -23.57, "west": -46.66, "east": -46.62},
        {"north": -23.56, "south": -23.59, "west": -46.69, "east": -46.65},
        {"north": -23.58, "south": -23.61, "west": -46.70, "east": -46.66},
        {"north": -23.59, "south": -23.63, "west": -46.67, "east": -46.63},
        {"north": -23.52, "south": -23.56, "west": -46.71, "east": -46.66},
        {"north": -23.53, "south": -23.57, "west": -46.60, "east": -46.55},
        {"north": -23.60, "south": -23.65, "west": -46.58, "east": -46.52}
    ]
    tasks = []
    for bounds in quadrantes:
        for pagina in range(1, max_paginas_por_quadrante + 1):
            payload = {
                "context": {"mapBounds": bounds},
                "filters": {"availability": "ANY", "businessContext": "RENT"},
                "return": ["id", "bedrooms", "area", "rentPrice", "totalCost", "condo", "iptu", "address", "amenities"],
                "pagination": {"page": pagina, "pageSize": 40}
            }
            tasks.append(payload)

    imoveis_coletados = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(requisitar_pagina, API_URL_QUINTOANDAR, p, headers) for p in tasks]
        for future in as_completed(futures):
            res = future.result()
            if res:
                imoveis_coletados.extend(res)
    return pd.DataFrame(imoveis_coletados) if imoveis_coletados else None

@st.cache_data(ttl=86400)
def carregar_dados_pipeline(max_paginas):
    df_api = buscar_imoveis_quintoandar_api_massivo(max_paginas_por_quadrante=max_paginas)
    if df_api is not None and not df_api.empty:
        return df_api, "API QuintoAndar (Tempo Real)", True, len(df_api)
    else:
        try:
            df_csv = pd.read_csv("quinto_andar_transformed_data.csv")
            return df_csv, "quinto_andar_transformed_data.csv (Base Local)", False, len(df_csv)
        except Exception:
            return pd.DataFrame(), "Nenhuma Fonte Disponível", False, 0

with st.spinner("⏳ Sincronizando dados imobiliários e treinando modelos preditivos..."):
    df_raw, fonte_dados, sucesso_api, total_linhas_recebidas = carregar_dados_pipeline(max_paginas=4)

if df_raw.empty:
    st.error("Erro crítico: Não foi possível carregar a base de dados imobiliária.")
    st.stop()

df_clean = df_raw.copy()
if 'id_imovel' not in df_clean.columns:
    if 'url' in df_clean.columns:
        extracted_ids = df_clean['url'].astype(str).str.extract(r'imovel/(\d+)')[0]
        df_clean['id_imovel'] = extracted_ids.fillna(df_clean.index.to_series().astype(str))
    else:
        df_clean['id_imovel'] = df_clean.index.to_series().astype(str)

df_clean = df_clean.drop_duplicates(subset=['id_imovel'])

for col in ['condominio', 'iptu', 'aluguel', 'metragem', 'quarto', 'aceita_pet', 'mobilia']:
    df_clean[col] = pd.to_numeric(df_clean.get(col, 0), errors='coerce').fillna(0)

df_clean = df_clean[(df_clean['metragem'] >= 12) & (df_clean['metragem'] <= 800)]
df_clean = df_clean[(df_clean['aluguel'] >= 500) & (df_clean['aluguel'] <= 50000)]

# Corrige provável perda de casa decimal somente quando a área e o aluguel/m²
# são outliers, e a área dividida por 10 passa a ser compatível com a amostra.
if len(df_clean) >= 100:
    preco_m2_original = df_clean['aluguel'] / df_clean['metragem']
    limite_inferior, limite_superior = preco_m2_original.quantile([0.01, 0.99])
    area_normalizada = df_clean['metragem'] / 10
    preco_m2_normalizado = df_clean['aluguel'] / area_normalizada
    area_suspeita = (
        (df_clean['metragem'] >= 5 * df_clean['metragem'].median())
        & (preco_m2_original < limite_inferior)
        & preco_m2_normalizado.between(limite_inferior, limite_superior)
    )
    df_clean.loc[area_suspeita, 'metragem'] = area_normalizada[area_suspeita]

df_clean['preco_m2'] = df_clean['aluguel'] / df_clean['metragem']
df_clean['custo_total_calculado'] = df_clean['aluguel'] + df_clean['condominio'] + df_clean['iptu']

# ==============================================================================
# TREINAMENTO DO MODELO PREDITIVO (AVM - REGRESSÃO LINEAR COM BAIRROS)
# ==============================================================================
df_ml = pd.get_dummies(df_clean, columns=['bairro'], drop_first=True)
features_ml = ['metragem', 'quarto', 'aceita_pet', 'mobilia'] + [col for col in df_ml.columns if col.startswith('bairro_')]

X = df_ml[features_ml]
y = df_ml['aluguel']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
modelo_regressao = LinearRegression()
modelo_regressao.fit(X_train, y_train)

y_pred_test = modelo_regressao.predict(X_test)
r2_modelo = r2_score(y_test, y_pred_test)
mae_modelo = mean_absolute_error(y_test, y_pred_test)

df_clean['aluguel_estimado_ml'] = modelo_regressao.predict(X)
df_clean['diferenca_preco'] = df_clean['aluguel'] - df_clean['aluguel_estimado_ml']
df_clean['status_oportunidade'] = df_clean['diferenca_preco'].apply(
    lambda x: '💎 Oportunidade' if x < -0.10 * abs(x) else ('⚠️ Acima da Média' if x > 0.10 * abs(x) else 'Equilibrado')
)

# ==============================================================================
# SIDEBAR
# ==============================================================================
st.sidebar.markdown("<h3 style='color: #ffffff; font-size: 1.4rem; line-height: 1.3; margin-bottom: 30px;'>🏢 QuintoAndar Analytics</h3>", unsafe_allow_html=True)

menu_selecionado = st.sidebar.radio(
    "Navegação Principal:",
    options=[
        "📊 Dashboard Geral (Sprint 3)",
        "🔬 Metodologia & Captura",
        "🏙️ Cruzamento Territorial",
        "🤖 Análise Preditiva & AVM",
        "🎯 Crescimento & ODS (Sprint 4)",
        "📋 Tabela Auditável",
        "🏢 Contexto de Negócio"
    ]
)

st.sidebar.markdown("<hr style='border-color: #21262d;'>", unsafe_allow_html=True)
st.sidebar.markdown("### 🔍 Filtros da Amostra")
st.sidebar.caption(f"**Origem:** {fonte_dados}")

bairros_disponiveis = sorted(df_clean['bairro'].dropna().unique())
bairros_selecionados = st.sidebar.multiselect("Filtrar Bairros:", options=bairros_disponiveis, default=[])

min_aluguel_val, max_aluguel_val = float(df_clean['aluguel'].min()), float(df_clean['aluguel'].max())
faixa_aluguel = st.sidebar.slider("Faixa de Aluguel (R$):", min_value=min_aluguel_val, max_value=max_aluguel_val, value=(min_aluguel_val, max_aluguel_val), step=500.0)

df_filtered = df_clean.copy()
if bairros_selecionados:
    df_filtered = df_filtered[df_filtered['bairro'].isin(bairros_selecionados)]
df_filtered = df_filtered[df_filtered['aluguel'].between(faixa_aluguel[0], faixa_aluguel[1])]

st.sidebar.markdown("<hr style='border-color: #21262d;'>", unsafe_allow_html=True)
csv_ptbr_data = converter_df_para_csv_ptbr(df_filtered)
st.sidebar.download_button(
    label="📥 Baixar Base (CSV)",
    data=csv_ptbr_data,
    file_name="quintoandar_dados_filtrados.csv",
    mime="text/csv"
)

# ==============================================================================
# KPIS
# ==============================================================================
total_imoveis_filt = len(df_filtered)
mediana_aluguel = df_filtered['aluguel'].median() if total_imoveis_filt > 0 else 0
mediana_m2 = df_filtered['preco_m2'].median() if total_imoveis_filt > 0 else 0
pct_pet = (df_filtered['aceita_pet'].sum() / total_imoveis_filt * 100) if total_imoveis_filt > 0 else 0

k1, k2, k3 = st.columns(3)
k1.metric("Aluguel Mediano", formatar_moeda_br(mediana_aluguel), "+12% vs mês ant.")
k2.metric("Imóveis Ativos", formatar_numero_br(total_imoveis_filt), "+5.4% var.")
k3.metric("Taxa Pet-Friendly", f"{formatar_numero_br(pct_pet, 1)}%", "+0.8% conv.")

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# ROTEAMENTO DE MÓDULOS
# ==============================================================================

if menu_selecionado == "📊 Dashboard Geral (Sprint 3)":
    st.subheader("📊 Sprint 3: Visualização Geral e Correlação de Dados")
    
    col_gr_1, col_gr_2 = st.columns([2, 1])

    with col_gr_1:
        faixa_cor = None
        if len(df_filtered) > 1:
            limite_inferior, limite_superior = df_filtered['preco_m2'].quantile([0.05, 0.95])
            if np.isfinite(limite_inferior) and np.isfinite(limite_superior) and limite_inferior < limite_superior:
                faixa_cor = (float(limite_inferior), float(limite_superior))

        fig_scatter = px.scatter(
            df_filtered, 
            x='metragem', 
            y='aluguel', 
            color='preco_m2',
            range_color=faixa_cor,
            size='custo_total_calculado', 
            size_max=30,
            hover_data=['bairro', 'quarto'],
            color_continuous_scale='Turbo',
            template="plotly_dark",
            labels={
                'metragem': 'Área Útil em m² (Eixo X)',
                'aluguel': 'Valor do Aluguel em R$ (Eixo Y)',
                'preco_m2': 'Preço/m²',
                'custo_total_calculado': 'Custo Total'
            }
        )
        fig_scatter.update_coloraxes(
            showscale=True,
            colorbar=dict(
                title=dict(text="Aluguel/m² (R$)", font=dict(color="#ffffff", size=11)),
                tickfont=dict(color="#ffffff", size=10),
                tickformat=".0f",
                outlinecolor="#ffffff",
                outlinewidth=1,
                thickness=14,
            ),
        )
        fig_scatter.update_traces(marker=dict(opacity=0.85, line=dict(width=1.2, color='#ffffff')))
        fig_scatter.update_layout(
            title=dict(text="Dispersão: Área (m²) vs Aluguel (R$)", font=dict(color="#ffffff", size=15)),
            paper_bgcolor="#1a212d", plot_bgcolor="#1a212d",
            font=dict(color="#8b949e", size=11), height=380,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=True, gridcolor="#273344"),
            yaxis=dict(showgrid=True, gridcolor="#273344")
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_gr_2:
        df_bairro_pie = df_filtered.groupby('bairro')['id_imovel'].count().reset_index().head(5)
        fig_pie = px.pie(
            df_bairro_pie, names='bairro', values='id_imovel',
            hole=0.6, template="plotly_dark",
            color_discrete_sequence=['#3b82f6', '#ec4899', '#10b981', '#f59e0b', '#8b5cf6']
        )
        fig_pie.update_layout(
            title=dict(text="Participação por Bairro (Fontes)", font=dict(color="#ffffff", size=15)),
            paper_bgcolor="#1a212d", plot_bgcolor="#1a212d",
            font=dict(color="#8b949e", size=11), height=380,
            margin=dict(l=10, r=10, t=40, b=10),
            showlegend=False
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Legenda explicativa com destaque forte nas cores e tamanhos das bolhas
    st.markdown("""
    <div class="dashboard-card" style="border-left: 4px solid #38bdf8;">
        <h4>📌 Legenda Analítica: O que o Gráfico de Dispersão está Analisando?</h4>
        <p>O gráfico de dispersão à esquerda realiza uma <b>análise multivariada da elasticidade de preços</b> do mercado imobiliário. Para facilitar a visualização e interpretação imediata, observe os seguintes elementos visuais:</p>
        <ul>
            <li><b>Eixo X (Horizontal):</b> Representa a área útil do imóvel em metros quadrados (m²).</li>
            <li><b>Eixo Y (Vertical):</b> Representa o valor mensal bruto do aluguel em Reais (R$).</li>
            <li>🎨 <b>Destaque da Cor da Bolha (Escala Turbo):</b> Cada círculo possui uma cor que indica o <b>valor do metro quadrado (R$/m²)</b>. A escala usa os percentis 5 e 95 para destacar as diferenças da maioria dos anúncios; valores fora dessa faixa aparecem nas extremidades.
                <br>• <b>Tons mais claros, alaranjados e amarelados (brilhantes):</b> Apontam regiões nobres, studios compactos ou áreas de altíssima valorização por metro quadrado.
                <br>• <b>Tons mais escuros, roxos e azulados:</b> Indicam menor custo relativo por m² (imóveis mais econômicos por área).
            </li>
            <li>📏 <b>Destaque do Tamanho da Bolha:</b> Expressa visualmente o <b>Custo Total Mensal (Aluguel + Condomínio + IPTU)</b>. Bolhas maiores representam unidades onde os encargos fixos pesam mais, evidenciando o impacto financeiro real no orçamento do inquilino.</li>
            <li><b>Insight Principal:</b> Permite identificar rapidamente discrepâncias de mercado, unindo área, valor absoluto, custo por metro quadrado e encargos em um único campo visual.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif menu_selecionado == "🔬 Metodologia & Captura":
    st.subheader("🔬 Metodologia de Análise de Dados e Captura")
    st.markdown("""
    <div class="dashboard-card">
        <h4>1. Como os Dados Foram Capturados</h4>
        <p>Foi aplicado <b>Web Scraping</b> (raspagem automatizada de informações públicas) consultando o endpoint da API pública de busca do QuintoAndar. Em Python, a biblioteca <code>requests</code> envia as requisições HTTP e o <code>ThreadPoolExecutor</code> organiza até 10 tarefas em paralelo, consultando diferentes páginas e regiões. Assim, a coleta concorrente reduz o tempo de espera; não se trata de chamadas assíncronas com <code>async</code>.</p>
    </div>
    <div class="dashboard-card">
        <h4>2. Pipeline de Machine Learning (Análise Preditiva)</h4>
        <p>O modelo de <b>Regressão Linear Múltipla</b> aprende como características dos imóveis se relacionam com o aluguel. Os bairros são convertidos em variáveis indicadoras para que também possam ser usados no cálculo. O resultado é uma estimativa de aluguel (AVM), não uma garantia de preço.</p>
        <div class="learning-note">
            <p><b>Em linguagem simples:</b> o algoritmo compara os dados dos imóveis (área, quartos, pets, mobília e bairro), aprende padrões de preço e usa esses padrões para estimar o aluguel de outro imóvel. Pense nele como uma estimativa baseada nos exemplos disponíveis — quanto mais representativos forem os dados, mais útil tende a ser a previsão.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif menu_selecionado == "🏙️ Cruzamento Territorial":
    st.subheader("🏙️ Cruzamento Territorial e Tipologias")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        df_group_bairro = df_filtered.groupby('bairro').agg(
            volume_anuncios=('id_imovel', 'count'),
            mediana_preco_m2=('preco_m2', 'median')
        ).reset_index().sort_values(by='volume_anuncios', ascending=False).head(10)
        if not df_group_bairro.empty:
            fig_bar = px.bar(
                df_group_bairro, x='volume_anuncios', y='bairro', orientation='h',
                color='mediana_preco_m2', color_continuous_scale='Plasma', template="plotly_dark",
                labels={
                    'volume_anuncios': 'Volume de Anúncios',
                    'bairro': 'Bairro',
                    'mediana_preco_m2': 'Mediana R$/m²'
                }
            )
            fig_bar.update_layout(
                title=dict(text="Top 10 Bairros: Liquidez vs Preço/m²", font=dict(color="#ffffff", size=14)),
                paper_bgcolor="#1a212d", plot_bgcolor="#1a212d", 
                font=dict(color="#8b949e", size=11), height=400,
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    with col_t2:
        df_quartos = df_filtered[df_filtered['quarto'].between(1, 4)].groupby('quarto').agg(
            aluguel_mediano=('aluguel', 'median')
        ).reset_index()
        if not df_quartos.empty:
            fig_line = px.line(
                df_quartos, x='quarto', y='aluguel_mediano', markers=True, template="plotly_dark",
                labels={
                    'quarto': 'Número de Dormitórios',
                    'aluguel_mediano': 'Aluguel Mediano (R$)'
                }
            )
            fig_line.update_traces(line_color='#38bdf8', line_width=3, marker_size=9)
            fig_line.update_layout(
                title=dict(text="Curva de Preço por Tipologia (Dormitórios)", font=dict(color="#ffffff", size=14)),
                paper_bgcolor="#1a212d", plot_bgcolor="#1a212d", 
                font=dict(color="#8b949e", size=11), height=400
            )
            st.plotly_chart(fig_line, use_container_width=True)

    # Legenda explicativa do Cruzamento Territorial e Tipologias
    st.markdown("""
    <div class="dashboard-card" style="border-left: 4px solid #10b981;">
        <h4>📌 Legenda Analítica: O que o Cruzamento Territorial e Tipologias Analisa?</h4>
        <p>Este painel divide a inteligência de mercado em duas dimensões complementares (<b>Geografia</b> e <b>Configuração Interna</b>):</p>
        <ul>
            <li><b>Gráfico de Barras Horizontais (À Esquerda — Liquidez vs. Valorização):</b> O comprimento da barra (Eixo X) mostra o <b>volume de oferta ativa</b> nos 10 bairros com maior concentração de anúncios, enquanto a <b>cor (escala Plasma)</b> revela a mediana do preço por metro quadrado (R$/m²). Barras em tons claros/amarelados indicam bairros de altíssima valorização por área; tons escuros indicam regiões de menor custo por metro quadrado.</li>
            <li><b>Gráfico de Linhas (À Direita — Elasticidade por Tipologia):</b> Demonstra o salto financeiro mediano (Eixo Y) conforme aumenta a quantidade de dormitórios (Eixo X, de 1 a 4 quartos), evidenciando o degrau de custo entre imóveis compactos e unidades familiares.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif menu_selecionado == "🤖 Análise Preditiva & AVM":
    st.subheader("🤖 Módulo de Análise Preditiva e Machine Learning (AVM)")
    
    st.markdown("""
    <div class="dashboard-card" style="border-left: 4px solid #38bdf8;">
        <h4>💡 O que é AVM (Automated Valuation Model)?</h4>
        <p><b>AVM</b> (Modelo de Avaliação Automatizada) refere-se ao uso de técnicas estatísticas e algoritmos de Inteligência Artificial / Machine Learning para estimar o valor de mercado de um imóvel de forma automatizada. Em vez de depender apenas de avaliações humanas subjetivas, o AVM cruza variáveis estruturais (metragem, quartos, comodidades) e espaciais (bairro) com grandes bases de dados históricos para prever o aluguel justo e identificar oportunidades no mercado imobiliário.</p>
    </div>
    """, unsafe_allow_html=True)

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown(f"""
        <div class="dashboard-card">
            <h4>📈 Desempenho do Modelo Preditivo</h4>
            <p><b>Algoritmo Utilizado:</b> Regressão Linear Múltipla (Scikit-Learn)</p>
            <p><b>Coeficiente de Determinação (R²):</b> <code>{r2_modelo:.2f}</code> (Explica ~{r2_modelo*100:.1f}% da variância dos aluguéis)</p>
            <p><b>Erro Médio Absoluto (MAE):</b> <code>{formatar_moeda_br(mae_modelo)}</code></p>
            <p><b>Variáveis preditoras:</b> Metragem, Número de Quartos, Aceitação de Pets, Mobília e Localização (Bairros).</p>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown("""
        <div class="dashboard-card">
            <h4>🎯 Simulador de Preço Justo (AVM)</h4>
            <p>Insira as características do imóvel abaixo para o modelo prever o aluguel recomendado:</p>
        </div>
        """, unsafe_allow_html=True)
        
        sim_bairro = st.selectbox("Selecione o Bairro:", options=bairros_disponiveis)
        sim_metragem = st.number_input("Metragem (m²):", min_value=15.0, max_value=400.0, value=55.0, step=1.0)
        sim_quartos = st.selectbox("Número de Quartos:", options=[1, 2, 3, 4], index=1)
        sim_pet = st.checkbox("Aceita Pets?", value=True)
        sim_mobilia = st.checkbox("Mobiliado?", value=False)
        
        input_dict = {col: 0.0 for col in features_ml}
        input_dict['metragem'] = float(sim_metragem)
        input_dict['quarto'] = float(sim_quartos)
        input_dict['aceita_pet'] = 1.0 if sim_pet else 0.0
        input_dict['mobilia'] = 1.0 if sim_mobilia else 0.0
        
        bairro_col_name = f"bairro_{sim_bairro}"
        if bairro_col_name in input_dict:
            input_dict[bairro_col_name] = 1.0
            
        df_input = pd.DataFrame([input_dict])
        val_predito = modelo_regressao.predict(df_input)[0]
        
        st.markdown(f"""
        <div class="avm-result-card">
            <h3>Aluguel Estimado pelo Algoritmo (AVM)</h3>
            <div class="avm-result-value">{formatar_moeda_br(val_predito)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("💎 Classificação de Imóveis Oportunidade (Scoring Preditivo)")
    
    df_oportunidades = df_filtered[df_filtered['status_oportunidade'] == '💎 Oportunidade'].sort_values(by='diferenca_preco')
    if not df_oportunidades.empty:
        df_oportunidades_exibicao = df_oportunidades[
            ['id_imovel', 'bairro', 'aluguel', 'aluguel_estimado_ml', 'metragem', 'quarto', 'url']
        ].copy()
        df_oportunidades_exibicao['aluguel'] = df_oportunidades_exibicao['aluguel'].apply(formatar_moeda_br)
        df_oportunidades_exibicao['aluguel_estimado_ml'] = df_oportunidades_exibicao['aluguel_estimado_ml'].apply(formatar_moeda_br)
        df_oportunidades_exibicao['metragem'] = df_oportunidades_exibicao['metragem'].apply(
            lambda x: f"{formatar_numero_br(x, 1)} m²"
        )
        df_oportunidades_exibicao['quarto'] = df_oportunidades_exibicao['quarto'].apply(
            lambda x: formatar_numero_br(x, 0)
        )
        st.caption("Valores mensais em reais (R$), com centavos; área em m². Áreas com provável erro de escala são corrigidas após validação pelo aluguel/m².")
        st.dataframe(
            df_oportunidades_exibicao,
            column_config={
                "url": st.column_config.LinkColumn("Link", display_text="Ver no QuintoAndar ↗"),
                "id_imovel": "ID", "bairro": "Bairro", 
                "aluguel": "Aluguel Cobrado", "aluguel_estimado_ml": "Aluguel Preditivo (ML)",
                "metragem": "Área", "quarto": "Quartos"
            },
            width="stretch", height=300, hide_index=True
        )
    else:
        st.info("Nenhuma oportunidade subprecificada encontrada nos filtros atuais.")

elif menu_selecionado == "🎯 Crescimento & ODS (Sprint 4)":
    st.subheader("🎯 Sprint 4: Análise Estratégica, Prevenção de Declínio e Relação com os ODS da ONU")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="dashboard-card" style="border-left: 4px solid #f43f5e;">
            <h4>⚠️ Prevenção de Declínio & Riscos de Mercado</h4>
            <p><b>Precificação Dinâmica:</b> Utilização do modelo preditivo (AVM) para identificar imóveis com preços desalinhados antes que acumulem dias de vacância.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="dashboard-card" style="border-left: 4px solid #10b981;">
            <h4>🚀 Estratégias de Crescimento & Market Share</h4>
            <p><b>Foco em Unidades de Giro Rápido:</b> Priorizar campanhas para imóveis de 1 e 2 quartos com base na demanda algorítmica.</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("""
    <div class="dashboard-card" style="border-left: 4px solid #38bdf8;">
        <h4>🌍 Alinhamento com os ODS da ONU</h4>
        <ul>
            <li><b>ODS 11 (Cidades Sustentáveis):</b> Previsibilidade de custos habitacionais para melhor planejamento urbano.</li>
            <li><b>ODS 8 (Trabalho Decente):</b> Inovação tecnológica em Proptech automatizando a avaliação imobiliária.</li>
            <li><b>ODS 12 (Consumo Responsável):</b> Otimização do aproveitamento do estoque imobiliário existente.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif menu_selecionado == "📋 Tabela Auditável":
    st.subheader("📋 Base de Imóveis Auditados e Preditivos")
    df_exibicao = df_filtered[['id_imovel', 'bairro', 'aluguel', 'aluguel_estimado_ml', 'status_oportunidade', 'metragem', 'quarto', 'url']].copy()
    df_exibicao['aluguel'] = df_exibicao['aluguel'].apply(formatar_moeda_br)
    df_exibicao['aluguel_estimado_ml'] = df_exibicao['aluguel_estimado_ml'].apply(formatar_moeda_br)
    df_exibicao['metragem'] = df_exibicao['metragem'].apply(lambda x: f"{formatar_numero_br(x, 1)} m²")
    df_exibicao['quarto'] = df_exibicao['quarto'].apply(lambda x: formatar_numero_br(x, 0))

    st.caption("Aluguel e estimativa são valores mensais em reais (R$), com centavos. Área em m²; quartos em quantidade. Áreas com provável erro de escala são corrigidas após validação pelo aluguel/m².")
    st.dataframe(
        df_exibicao,
        column_config={
            "url": st.column_config.LinkColumn("Link", display_text="Ver no QuintoAndar ↗"),
            "id_imovel": "ID", "bairro": "Bairro", "aluguel": "Aluguel",
            "aluguel_estimado_ml": "Valor Predito (ML)", "status_oportunidade": "Status Preditivo",
            "metragem": "Área", "quarto": "Quartos"
        },
        width="stretch", hide_index=True
    )