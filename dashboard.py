from datetime import datetime
import plotly.express as px
import streamlit as st
import yfinance as yf

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Scorpion Finance | Radar de Mercado",
    page_icon="⚡",
    layout="wide",
)

# --- CSS CUSTOMIZADO (Design Limpo, Elegante e Profissional) ---
st.markdown(
    """
    <style>
    /* Fundo da aplicação */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Cabeçalhos */
    h1 {
        color: #58a6ff !important;
        font-weight: 700;
    }
    h2, h3 {
        color: #3fb950 !important;
    }
    
    /* Caixas de métricas */
    div[data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 12px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    div[data-testid="stMetricValue"] {
        color: #58a6ff !important;
        font-size: 22px !important;
        font-weight: bold;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #8b949e !important;
        font-size: 14px !important;
    }

    /* Ajuste para Caixas de Seleção e Inputs */
    div[data-baseweb="select"] > div {
        background-color: #161b22 !important;
        color: #f0f6fc !important;
        border-color: #30363d !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- TÍTULO DO DASHBOARD ---
st.title("⚡ SCORPION FINANCE — RADAR DE MERCADO")
st.caption(
    f"🌐 Inteligência e Análise Financeira em Tempo Real | Atualizado em:"
    f" {datetime.now().strftime('%d/%m/%Y %H:%M')}"
)

# --- DICIONÁRIO DE ATIVOS ---
categorias_ativos = {
    "Ações Brasileiras (B3)": {
        "Petrobras (PETR4)": "PETR4.SA",
        "Vale (VALE3)": "VALE3.SA",
        "Itaú Unibanco (ITUB4)": "ITUB4.SA",
        "Bradesco (BBDC4)": "BBDC4.SA",
        "Banco do Brasil (BBAS3)": "BBAS3.SA",
        "Eletrobras (ELET3)": "ELET3.SA",
        "Magazine Luiza (MGLU3)": "MGLU3.SA",
    },
    "Criptomoedas (R$)": {
        "Bitcoin (BTC)": "BTC-BRL",
        "Ethereum (ETH)": "ETH-BRL",
        "Solana (SOL)": "SOL-BRL",
    },
    "Índices & Câmbio": {
        "Ibovespa": "^BVSP",
        "S&P 500": "^GSPC",
        "Dólar Comercial": "BRL=X",
        "Euro": "EURBRL=X",
    },
    "Commodities": {
        "Ouro": "GC=F",
        "Petróleo Brent": "BZ=F",
        "Café Arábica": "KC=F",
        "Milho": "ZC=F",
    },
}

# --- BARRA LATERAL ---
st.sidebar.header("⚙️ Filtros do Painel")
categoria_sel = st.sidebar.selectbox(
    "Selecione a Categoria", list(categorias_ativos.keys())
)
periodo_sel = st.sidebar.selectbox(
    "Período Gráfico",
    ["1mo", "3mo", "6mo", "1y"],
    format_func=lambda x: {
        "1mo": "1 Mês",
        "3mo": "3 Meses",
        "6mo": "6 Meses",
        "1y": "1 Ano",
    }[x],
)

# --- DESTAQUES DO MERCADO ---
st.subheader(f"📌 Destaques — {categoria_sel}")
ativos = categorias_ativos[categoria_sel]
cols = st.columns(min(len(ativos), 4))

for index, (nome, ticker) in enumerate(ativos.items()):
  col_idx = index % 4
  try:
    ticker_data = yf.Ticker(ticker)
    df_recent = ticker_data.history(period="7d")

    if not df_recent.empty and len(df_recent) >= 2:
      preco_atual = df_recent["Close"].iloc[-1]
      preco_anterior = df_recent["Close"].iloc[-2]
      variacao = ((preco_atual - preco_anterior) / preco_anterior) * 100

      moeda = "R$" if ("BRL" in ticker or ".SA" in ticker) else "US$"
      cols[col_idx].metric(
          label=nome,
          value=f"{moeda} {preco_atual:,.2f}",
          delta=f"{variacao:+.2f}%",
      )
    else:
      cols[col_idx].write(f"⚠️ {nome}: Indisponível")
  except Exception:
    cols[col_idx].write(f"⚠️ {nome}: Erro de busca")

st.divider()

# --- ANÁLISE GRÁFICA HISTÓRICA ---
st.subheader("📈 Gráfico de Desempenho")
ativo_escolhido = st.selectbox(
    "Escolha o ativo para visualização detalhada:", list(ativos.keys())
)
ticker_escolhido = ativos[ativo_escolhido]

try:
  dados_grafico = yf.Ticker(ticker_escolhido).history(period=periodo_sel)

  if not dados_grafico.empty:
    fig = px.line(
        dados_grafico,
        x=dados_grafico.index,
        y="Close",
        title=f"Histórico de Fechamento — {ativo_escolhido}",
        labels={"Close": "Preço", "Date": "Data"},
    )
    fig.update_traces(line_color="#3fb950", line_width=2.5)
    fig.update_layout(
        paper_bgcolor="#0d1117",
        plot_bgcolor="#161b22",
        font_color="#c9d1d9",
        xaxis=dict(gridcolor="#21262d", showgrid=True),
        yaxis=dict(gridcolor="#21262d", showgrid=True, autorange=True),
        margin=dict(l=40, r=40, t=50, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)
  else:
    st.warning(
        f"Não foram encontrados dados históricos para {ativo_escolhido} no"
        " período selecionado."
    )
except Exception as err:
  st.error(f"Erro ao carregar o gráfico: {err}")
