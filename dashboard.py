from datetime import datetime
import plotly.express as px
import streamlit as st
import yfinance as yf

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Scorpion Finance | Dashboard", page_icon="📊", layout="wide"
)

st.title("📊 Scorpion Finance — Painel de Mercado em Tempo Real")
st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# --- DICIONÁRIO DE ATIVOS ---
categorias_ativos = {
    "Criptomoedas": {
        "Bitcoin": "BTC-USD",
        "Ethereum": "ETH-USD",
    },
    "Ações & Índices": {
        "Petrobras": "PETR4.SA",
        "Vale": "VALE3.SA",
        "Itaú": "ITUB4.SA",
        "Ibovespa": "^BVSP",
        "S&P 500": "^GSPC",
    },
    "Câmbio": {
        "Dólar": "BRL=X",
        "Euro": "EURBRL=X",
    },
    "Agronegócio & Commodities": {
        "Ouro": "GC=F",
        "Petróleo BRENT": "BZ=F",
        "Milho": "ZC=F",
        "Soja": "ZS=F",
        "Café Arábica": "KC=F",
    },
}

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.header("⚙️ Configurações")
categoria_sel = st.sidebar.selectbox(
    "Escolha a Categoria", list(categorias_ativos.keys())
)
periodo_sel = st.sidebar.selectbox(
    "Período do Histórico",
    ["1mo", "3mo", "6mo", "1y"],
    format_func=lambda x: {
        "1mo": "1 Mês",
        "3mo": "3 Meses",
        "6mo": "6 Meses",
        "1y": "1 Ano",
    }[x],
)

# --- CARDS DE INDICADORES (TOP) ---
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

      with cols[i]:
        st.metric(
            label=nome, value=f"{atual:,.2f}", delta=f"{var:+.2f}%"
        )
  except Exception as e:
    cols[i].write(f"Erro em {nome}")

st.divider()

# --- GRÁFICO INTERATIVO DE HISTÓRICO ---
st.subheader("📈 Análise Gráfica Histórica")
ativo_escolhido = st.selectbox(
    "Selecione um Ativo para visualizar o gráfico:",
    list(ativos_categoria.keys()),
)
ticker_escolhido = ativos_categoria[ativo_escolhido]

historico = yf.Ticker(ticker_escolhido).history(period=periodo_sel)

if not historico.empty:
  fig = px.line(
      historico,
      x=historico.index,
      y="Close",
      title=f"Evolução de Preço — {ativo_escolhido}",
      labels={"Close": "Preço de Fechamento", "Date": "Data"},
  )
  fig.update_traces(line_color="#27ae60", line_width=2)
  st.plotly_chart(fig, use_container_width=True)
else:
  st.warning("Não foi possível carregar os dados gráficos deste ativo.")
