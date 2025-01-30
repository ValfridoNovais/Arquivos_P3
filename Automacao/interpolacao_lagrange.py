import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sympy import symbols, expand, lambdify, simplify, pretty

# Configuração do Streamlit
st.set_page_config(page_title="Interpolação de Lagrange", layout="wide")

# Definição da variável simbólica
x = symbols('x')

# Função para calcular os polinômios base de Lagrange
def lagrange_basis(x_vals, i):
    numerador = 1
    denominador = 1
    for j in range(len(x_vals)):
        if i != j:
            numerador *= (x - x_vals[j])
            denominador *= (x_vals[i] - x_vals[j])
    return numerador / denominador

# Função para calcular o polinômio interpolador de Lagrange
def lagrange_interpolation(x_vals, y_vals):
    Pn = sum(y_vals[i] * lagrange_basis(x_vals, i) for i in range(len(x_vals)))
    return expand(Pn)

# Opções de entrada
st.sidebar.title("Entrada de Dados")
input_type = st.sidebar.radio("Escolha o tipo de entrada:", ["CSV", "XLSX", "JSON", "Manual"])

# Leitura dos dados
if input_type == "CSV":
    uploaded_file = st.sidebar.file_uploader("Envie um arquivo CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
elif input_type == "XLSX":
    uploaded_file = st.sidebar.file_uploader("Envie um arquivo XLSX", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
elif input_type == "JSON":
    uploaded_file = st.sidebar.file_uploader("Envie um arquivo JSON", type=["json"])
    if uploaded_file:
        df = pd.read_json(uploaded_file)
elif input_type == "Manual":
    st.sidebar.write("Digite os pontos manualmente:")
    manual_x = st.sidebar.text_input("Valores de X (separados por vírgula)", "1, 2, 3, 4")
    manual_y = st.sidebar.text_input("Valores de Y (separados por vírgula)", "2, 3, 5, 10")
    x_vals = list(map(float, manual_x.split(",")))
    y_vals = list(map(float, manual_y.split(",")))
    df = pd.DataFrame({"X": x_vals, "Y": y_vals})

# Se os dados foram carregados
if 'df' in locals():
    st.write("### 📊 Dados Carregados:")
    st.write(df)

    # Conversão dos dados
    x_vals = df["X"].values
    y_vals = df["Y"].values

    # Cálculo do polinômio interpolador
    Pn = lagrange_interpolation(x_vals, y_vals)
    st.write("### 📌 Polinômio Interpolador:")
    st.latex(f"P_n(x) = {Pn}")

    # 📌 **Mostrar cálculo passo a passo**
    st.write("## 🔍 Cálculo Passo a Passo")

    # 1️⃣ Fórmula Geral
    st.latex(r"P_n(x) = \sum_{i=0}^{n} f(x_i) L_i(x)")

    # 2️⃣ Mostrar cada \( L_i(x) \)
    st.write("### 🔹 Cálculo dos Polinômios Base \( L_i(x) \)")
    for i in range(len(x_vals)):
        L_i = expand(lagrange_basis(x_vals, i))
        st.latex(f"L_{i}(x) = {pretty(L_i)}")

    # 3️⃣ Mostrar termos individuais antes da soma
    st.write("### 🔹 Construção do Polinômio Interpolador")
    terms = [f"{y_vals[i]} \\cdot ({pretty(expand(lagrange_basis(x_vals, i)))})" for i in range(len(x_vals))]
    st.latex(r"P_n(x) = " + " + ".join(terms))

    # 4️⃣ Polinômio final expandido
    st.write("### 🔹 Polinômio Expandido Final")
    st.latex(f"P_n(x) = {pretty(Pn)}")

    # 📊 **Criar gráficos**
    Pn_func = lambdify(x, Pn, "numpy")
    x_plot = np.linspace(min(x_vals) - 1, max(x_vals) + 1, 1000)
    y_plot = Pn_func(x_plot)

    # 📊 **Gráfico 1 - Polinômio Completo**
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=x_plot, y=y_plot, mode="lines", name="Interpolador"))
    fig1.add_trace(go.Scatter(x=x_vals, y=y_vals, mode="markers", marker=dict(size=8, color="red"), name="Pontos Dados"))
    fig1.update_layout(title="Polinômio Interpolador", xaxis_title="X", yaxis_title="P(X)", template="plotly_white")

    # 📊 **Gráfico 2 - Funções Base**
    fig2 = go.Figure()
    L_funcs = []

    for i in range(len(x_vals)):
        L_i = expand(lagrange_basis(x_vals, i))
        L_func = lambdify(x, L_i, "numpy")
        L_funcs.append((L_i, L_func))
        fig2.add_trace(go.Scatter(x=x_plot, y=L_func(x_plot), mode="lines", name=f"L_{i}(x)"))

    fig2.update_layout(title="Polinômios Base de Lagrange", xaxis_title="X", yaxis_title="L_i(X)", template="plotly_white")

    # **Adicionar Filtro para Selecionar Funções Individuais**
    selected_L = st.selectbox("Escolha uma função base para visualizar", [f"L_{i}(x)" for i in range(len(x_vals))])
    index = int(selected_L.split("_")[1][0])
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=x_plot, y=L_funcs[index][1](x_plot), mode="lines", name=selected_L))
    fig3.update_layout(title=f"Polinômio Base {selected_L}", xaxis_title="X", yaxis_title=selected_L, template="plotly_white")

    # **Exibir os gráficos**
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)
