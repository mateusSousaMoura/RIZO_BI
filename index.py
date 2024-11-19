import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from app import app
from controllers import genero_dropdown, valor_slider, mes_slider
import pathlib
BASE_DIR = pathlib.Path(__file__).parent.resolve()

# Lendo o arquivo CSV
file_path =BASE_DIR / 'dados_doacao.csv'  # Certifique-se de colocar o caminho correto para o arquivo
data = pd.read_csv(file_path)

# Layout da aplicação
app.layout = dbc.Container(
    [
        # Título
        html.H1(
            "Dashboard de Doações",
            className="text-center mt-4 mb-4",
            style={
                "font-family": "'Sitka Subheading', monospace",
                "color": "#4f2239",  # Rosa
                "text-shadow": "2px 2px 4px #ff1493",  # Rosa forte
            },
        ),
        
        # Controles de Filtros
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        genero_dropdown,
                        style={
                            "font-family": "'Sitka Subheading', monospace",
                            "color": "#4f2239",  # Rosa
                            "background-color": "#ffb6c1",  # Rosa claro
                            "padding": "20px",
                            "border-radius": "10px",
                            "box-shadow": "2px 2px 10px rgba(0, 0, 0, 0.1)",
                        },
                    ),
                    md=6,
                ),
                dbc.Col(
                    dcc.Graph(id="grafico-genero"),
                    md=6,
                    style={
                        "background-color": "#ffe4e1",  # Rosa pêssego
                        "padding": "15px",
                        "border-radius": "10px",
                        "box-shadow": "2px 2px 10px rgba(0, 0, 0, 0.1)",
                    },
                ),

            ],
            className="mb-4",
        ),

        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        valor_slider,
                        style={
                            "font-family": "'Sitka Subheading', monospace",
                            "color": "#4f2239",  # Rosa
                            "background-color": "#ffb6c1",  # Rosa claro
                            "padding": "20px",
                            "border-radius": "10px",
                            "box-shadow": "2px 2px 10px rgba(0, 0, 0, 0.1)",
                        },
                    ),
                    md=6,
                ),
                dbc.Col(
                    dcc.Graph(id="grafico-histograma"),
                    md=6,
                    style={
                        "background-color": "#ffe4e1",  # Rosa pêssego
                        "padding": "15px",
                        "border-radius": "10px",
                        "box-shadow": "2px 2px 10px rgba(0, 0, 0, 0.1)",
                    },
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        mes_slider,
                        style={
                            "font-family": "'Sitka Subheading', monospace",
                            "color": "#4f2239",
                            "background-color": "#ffb6c1",
                            "padding": "20px",
                            "border-radius": "10px",
                            "box-shadow": "2px 2px 10px rgba(0, 0, 0, 0.1)",
                        },
                    ),
                    md=6,
                ),
                dbc.Col(
                    dcc.Graph(id="grafico-evolucao"),
                    md=12,
                    style={
                        "background-color": "#ffe4e1",
                        "padding": "15px",
                        "border-radius": "10px",
                        "box-shadow": "2px 2px 10px rgba(0, 0, 0, 0.1)",
                    },
                ),
            ]
        ),
    ],
    fluid=True,
    style={
        "background-color": "#f5cbd2",  # Fundo rosa claro
        "padding": "20px",
        "font-family": "'Comic Sans MS', cursive, sans-serif",
    },
)


# Callback para atualizar o gráfico de pizza com base no filtro de gêneros
@app.callback(
    Output("grafico-genero", "figure"),
    Input("genero-filter", "value"),
)
def update_genero_chart(selected_generos):
    filtered_data = data[data["Gênero"].isin(selected_generos)]

    color_map = {
        "Masculino": "#87CEFA",  # Light Blue
        "Feminino": "#FF69B4",  # Pink
        "Não-binário": "#FFD700",  # Gold
    }

    fig_pizza = px.pie(
        filtered_data,
        names="Gênero",
        values="Valor Doação",
        title="Doações por Gênero",
         color="Gênero",
        color_discrete_map= color_map,
    )
    return fig_pizza


# Callback para atualizar o histograma com base no filtro de valores
@app.callback(
    Output("grafico-histograma", "figure"),
    Input("valor-slider", "value"),
)
def update_histograma_chart(selected_range):
    filtered_data = data[
        (data["Valor Doação"] >= selected_range[0]) & (data["Valor Doação"] <= selected_range[1])
    ]
    fig_histograma = px.histogram(
        filtered_data,
        x="Valor Doação",
        nbins=20,
        title="Histograma de Valores de Doação",
        labels={"Valor Doação": "Valor da Doação"},
    )
    return fig_histograma

@app.callback(
    Output("grafico-evolucao", "figure"),
    [
        Input("mes-slider", "value"),
    ],
)
def update_evolucao_chart(selected_months):
    # Filtrar os dados pelo intervalo de meses
    start_month, end_month = selected_months
    data["Mês"] = pd.to_datetime(data["Data Doação"]).dt.month
    filtered_data = data[(data["Mês"] >= start_month) & (data["Mês"] <= end_month)]

    # Agrupar os dados por mês e calcular o somatório
    monthly_data = (
        filtered_data.groupby("Mês")["Valor Doação"]
        .sum()
        .reset_index()
        .sort_values("Mês")
    )

    # Criar o gráfico de linha
    fig_evolucao = px.line(
        monthly_data,
        x="Mês",
        y="Valor Doação",
        title="Evolução das Doações por Mês",
        markers=True,
        labels={"Mês": "Mês", "Valor Doação": "Somatório das Doações"},
    )
    fig_evolucao.update_traces(line=dict(color="#ff69b4"))  # Cor rosa para a linha
    fig_evolucao.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=list(range(1, 13)),
            ticktext=[
                "Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"
            ],
        ),
        plot_bgcolor="#fff0f5",  # Fundo rosa claro
        paper_bgcolor="#fff0f5",
    )
    return fig_evolucao


# Inicializando o servidor
if __name__ == "__main__":
    app.run_server(debug=True)
