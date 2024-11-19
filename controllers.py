from dash import dcc, html
import dash_bootstrap_components as dbc

# Controlador para escolher os gêneros
genero_dropdown = dbc.Form(
    [
        dbc.Label("Selecione os Gêneros:", html_for="genero-filter"),
        dcc.Dropdown(
            id="genero-filter",
            options=[
                {"label": "Masculino", "value": "Masculino"},
                {"label": "Feminino", "value": "Feminino"},
                {"label": "Não-binário", "value": "Não-binário"},
            ],
            value=["Masculino", "Feminino", "Não-binário"],
            multi=True,
        ),
    ],
    className="mb-4",
)

# Controlador para filtrar faixa de valores no histograma
valor_slider = dbc.Form(
    [
        dbc.Label("Filtrar Faixa de Valores de Doação:", html_for="valor-slider"),
        dcc.RangeSlider(
            id="valor-slider",
            min=0,
            max=1000,
            step=10,
            marks={i: f"{i}" for i in range(0, 1100, 200)},
            value=[0, 1000],
        ),
    ],
    className="mb-4",
)


mes_slider = dbc.Form(
    [
        dbc.Label("Selecione o Intervalo de Meses:", html_for="mes-slider"),
        dcc.RangeSlider(
            id="mes-slider",
            min=1,
            max=12,
            step=1,
            marks={i: f"{i}" for i in range(1, 13)},
            value=[1, 12],  # Inicialmente todo o ano
        ),
    ],
    className="mb-4",
)