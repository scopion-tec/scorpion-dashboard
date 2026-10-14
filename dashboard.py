from datetime import datetime
import plotly.express as px
import streamlit as st
import yfinance as yf

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Scorpion Finance | Dashboard", page_icon="⚡", layout="wide"
)

# Estilização CSS Customizada para Visual Agressivo/Dark Mode
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: bold;
        color: #00FF66;
    }
    div[data-testid="stMetric"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        padding: 15px;
        border-radius: 10px;
    }
    h1, h2, h3 {
        color: #00FF66 !important;
        font-family: 'Trebuchet MS', sans-serif;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("⚡ SCORPION FINANCE — RADAR DE MERCADO")
st.caption(
    f"🌐 Inteligência em Dados Financeiros | Última atualização:"
    f" {datetime.now().strftime('%d/%m/%Y %H:%M')}"
)

# --- DICIONÁRIO DE ATIVOS EXPANDIDO ---
categorias_ativos = {
    "Criptomoedas (R$)": {
        "Bitcoin (R$)": "BTC-BRL",
        "Ethereum (R$)": "ETH-BRL",
        "Solana (R$)": "SOL-BRL",
        "Cardano (R$)": "ADA-BRL",
    },
    "Ações Brasileiras (B3)": {
        "Petrobras PN": "PETR4.SA",
        "Petrobras ON": "PETR3.SA",
        "Vale": "VALE3.SA",
        "Itaú Unibanco": "ITUB4.SA",
        "Bradesco": "BBDC4.SA",
        "Banco do Brasil": "BBAS3.SA",
        "B3 SA": "B3SA3.SA",
        "WEG": "WEGE3.SA",
        "Magazine Luiza": "MGLU3.SA",
        "Ambev": "ABEV3.SA",
        "Eletrobras": "ELET3.SA",
        "Localiza": "RENT3.SA",
    },
    "Índices Globais": {
        "Ibovespa (Brasil)": "^BVSP",
        "S&P 500 (EUA)": "^GSPC",
        "Nasdaq (Tech EUA)": "^IXIC",
        "Dow Jones": "^DJI",
    },
    "Câmbio": {
        "Dólar Comercial": "BRL=X",
        "Euro": "EURBRL=X",
        "Libra Esterlina": "GBPBRL=X",
    },
    "Commodities": {
        "Ouro": "GC=F",
        "Petróleo BRENT": "BZ=F",
        "Milho": "ZC=F",
        "Soja": "ZS=F",
        "Café Arábica": "KC=F",
    },
}

# --- BARRA LATERAL ---
st.sidebar.header("⚙️ Painel de Controle")
categoria_sel = st.sidebar.selectbox(
    "Escolha o Mercado", list(categorias_ativos.keys())
)
periodo_sel = st.sidebar.selectbox(
    "Período Histórico",
    ["1mo", "3mo", "6mo", "1y"],
    format_func=lambda x: {
        "1mo": "1 Mês",
        "3mo": "3 Meses",
        "6mo": "6 Meses",
        "1y": "1 Ano",
    }[x],
)

# --- CARDS DE INDICADORES ---
st.subheader(f"📌 Destaques — {categoria_sel}")
ativos_categoria = categorias_ativos[categoria_sel]
cols = st.columns(len(ativos_categoria))

for i, (nome, ticker) in enumerate(ativos_categoria.items()):
  try:
    dados = yf.Ticker(ticker).history(period="5d")
    if len(dados) >= 2:
      atual = dados["Close"].iloc[-1]
      anterior = dados["Close"].iloc[-2]
      var = ((atual - anterior) / anterior) * 100

      simbolo = "R$" if "BRL" in ticker or ".SA" in ticker else "US$"
      with cols[i]:
        st.metric(
            label=nome, value=f"{simbolo} {atual:,.2f}", delta=f"{var:+.2f}%"
        )
  except Exception as e:
    cols[i].write(f"Erro em {nome}")

st.divider()

# --- GRÁFICO DARK NEON COM MARGENS AJUSTADAS ---
st.subheader("📈 Análise Gráfica Histórica")
ativo_escolhido = st.selectbox(
    "Selecione o Ativo para Análise:", list(ativos_categoria.keys())
)
ticker_escolhido = ativos_categoria[ativo_escolhido]

historico = yf.Ticker(ticker_escolhido).history(period=periodo_sel)

if not historico.empty:
  fig = px.area(
      historico,
      x=historico.index,
      y="Close",
      title=f"Evolução — {ativo_escolhido}",
      labels={"Close": "Preço de Fechamento", "Date": "Data"},
  )
  fig.update_traces(line_color="#00FF66", fillcolor="rgba(0, 255, 102, 0.1)")
  fig.update_layout(
      paper_bgcolor="#0E1117",
      plot_bgcolor="#161B22",
      font_color="#FFFFFF",
      margin=dict(t=50, b=40, l=40, r=40),
      xaxis=dict(gridcolor="#30363D"),
      yaxis=dict(gridcolor="#30363D", autorange=True),
  )
  st.plotly_chart(fig, use_container_width=True)
else:
  st.warning("Não foi possível carregar os dados deste ativo.")
