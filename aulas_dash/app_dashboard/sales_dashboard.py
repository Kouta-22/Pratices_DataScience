import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Carregando o arquivo CSV
df = pd.read_csv(r'C:\Users\Guilherme\OneDrive\Área de Trabalho\Pratices_DataScience\aulas_dash\data\sales_data_sample.csv', encoding='latin1')
global_df = df.copy()

global_df['Data_Pedido'] = pd.to_datetime(global_df['ORDERDATE'])
global_df['Ano'] = global_df['Data_Pedido'].dt.year
global_df['Meses'] = global_df['Data_Pedido'].dt.month_name()

drop_cols = ['ADDRESSLINE1', 'ADDRESSLINE2', 'POSTALCODE','CITY', 'TERRITORY', 'PHONE', 'CONTACTFIRSTNAME','CONTACTLASTNAME','CUSTOMERNAME','ORDERNUMBER']
global_df = global_df.drop(drop_cols, axis=1)

global_pais_ano_status_df = global_df.groupby(['COUNTRY','Ano','STATUS'])[['SALES']].mean()
global_pais_ano_status_df.reset_index(inplace=True)

global_pais_ano_status_PRODUCTLINE = global_df.groupby(['COUNTRY','Ano','STATUS','PRODUCTLINE','DEALSIZE'])[['SALES']].mean()
global_pais_ano_status_PRODUCTLINE.reset_index(inplace=True)

sales_data_df = global_df.groupby(['COUNTRY','Data_Pedido','DEALSIZE'])[['SALES']].mean()
sales_data_df.reset_index(inplace=True)

colors = {
    'background': '#f5f5f5',  # Fundo branco-cinza
    'text': '#000000',        # Texto preto
    'bar_border': '#888888'   # Cor da borda das barras
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY],
                meta_tags=[{'name':'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Dashboard Vendas',
                        className='text-center text-primary display-2 shadow'),
                width=10),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardImg(
                        src="assets/git-logo.jpg",
                        top=True,
                        bottom=False),
                    dbc.CardBody(
                        html.P("GitHub",
                               className="card text-white bg-primary text-center")
                    ),
                    dbc.CardLink('Meu GitHub webPage', href='https://github.com/Kouta-22/Pratices_DataScience',
                                 target='_blank', className='text-center'),
                ],
                style={"width": "18rem"},
            ),
            width={'size': 2, 'order': 2}
        ),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='dropdown-1',
                         multi=False,
                         value='Classic Cars',
                         options=[
                             {'label': x, 'value': x}
                             for x in df['PRODUCTLINE'].unique()
                         ]),
            dcc.Graph(id='bar-fig', figure={})
        ], width={'size': 4, 'order': 1}),
        dbc.Col([
            dcc.Dropdown(id='dropdown-2',
                         multi=True,
                         value=['USA'],
                         options=[
                             {'label': x, 'value': x}
                             for x in sales_data_df['COUNTRY'].unique()
                         ]),
            dcc.Graph(id='line-fig2', figure={})
        ], width={'size': 4, 'order': 2}),
        dbc.Col([
            dcc.Dropdown(id="dropdown-3",
                         options=[
                             {"label": "STATUS", "value": 'STATUS'},
                             {"label": "COUNTRY", "value": 'COUNTRY'},
                             {"label": "DEALSIZE", "value": 'DEALSIZE'},
                             {"label": "ANO", "value": 'Ano'}],
                         multi=False,
                         value='Ano',
                         style={'width': "60%"}, className="text-center"
                         ),
            dcc.Graph(id='pie-fig3', figure={})
        ], width={'size': 4, 'order': 3}),
    ]),
    dbc.Row([
        dbc.Col([
            html.P('Escolha o tamanho do Produto',
                   style={'textDecoration': 'underline'}),
            dcc.Checklist(id='minha-checklist', value=['Small'],
                          options=[{'label': x, 'value': x}
                                   for x in sales_data_df['DEALSIZE'].unique()],
                          labelClassName='mr-3 text-secondary'),
            dcc.Graph(id='fig_hist', figure={})
        ], width={'size': 6, 'order': 1}),

        dbc.Col([
            html.H1(id='output_title', children=[],
                    style={'text-align': 'center'}),
            dcc.Dropdown(id='ano_selecionado',
                         options=[
                             {'label': 'Ano: 2003', 'value': 2003},
                             {'label': 'Ano: 2004', 'value': 2004},
                             {'label': 'Ano: 2005', 'value': 2005},
                         ],
                         multi=False,
                         value=2003,
                         style={'width': "60%"}, className="text-center"
                         ),
            dcc.Graph(id='mapa_de_vendas', figure={})
        ], width={'size': 6, 'order': 2})
    ]),
], fluid=True)


@app.callback(
    Output('bar-fig', 'figure'),
    Input('dropdown-1', 'value')
)
def update_bar_chart_1(produto_selecionado):
    dff = df[df['PRODUCTLINE'] == produto_selecionado]

    figln = px.bar(dff, x='SALES', y='COUNTRY',
                   orientation='h',
                   color_discrete_sequence=px.colors.sequential.gray)
    
    figln.update_traces(marker=dict(line=dict(width=1, color=colors['bar_border'])))
    
    figln.update_xaxes(showgrid=False)
    figln.update_yaxes(showgrid=False)

    figln.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        title={
            'text': f'Vendas por País para {produto_selecionado}',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Vendas',
        yaxis_title='País',
        margin=dict(l=0, r=0, t=30, b=0),
        height=400
    )
    return figln


@app.callback(
    Output('line-fig2', 'figure'),
    Input('dropdown-2', 'value')
)
def update_line_grap(pais_selecionado):
    dff = sales_data_df[sales_data_df['COUNTRY'].isin(pais_selecionado)]

    figln2 = px.line(dff, x='Data_Pedido', y='SALES', color='COUNTRY',
                     color_discrete_sequence=px.colors.qualitative.Prism)
    
    figln2.update_xaxes(showgrid=False)
    figln2.update_yaxes(showgrid=True)
    figln2.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return figln2


@app.callback(
    Output('pie-fig3', 'figure'),
    Input('dropdown-3', 'value')
)
def update_pie_grap(info):
    figln3 = px.pie(global_df, names=info, hole=.3)

    figln3.update_xaxes(showgrid=False)
    figln3.update_yaxes(gridcolor='#839496')

    figln3.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return figln3


@app.callback(
    Output('fig_hist', 'figure'),
    Input('minha-checklist', 'value')
)
def update_hist_checklist(tamanho_selecionado):
    dff = global_df[global_df['DEALSIZE'].isin(tamanho_selecionado)]

    fig_hist = px.histogram(dff, x='COUNTRY', y='SALES',
                            color_discrete_sequence=px.colors.qualitative.Prism)
    
    fig_hist.update_xaxes(showgrid=False)
    fig_hist.update_yaxes(showgrid=False)

    fig_hist.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig_hist


@app.callback(
    [Output(component_id='output_title', component_property='children'),
     Output(component_id='mapa_de_vendas', component_property='figure')],
    [Input(component_id='ano_selecionado', component_property='value')]
)
def update_map(ano_selecioado):
    title = f'Mapa de vendas nos EUA no ano de {ano_selecioado}'

    df_ = global_df.copy()
    df_ = df_[df_['COUNTRY'] == 'USA']
    df_ = df_[df_['Ano'] == ano_selecioado]
    df_ = df_[df_["STATUS"] == "Shipped"]
    
    fig = px.choropleth(
        data_frame=df_,
        locationmode='USA-states',
        locations='STATE',
        scope='usa',
        color='SALES',
        hover_data=['STATE', 'SALES'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        template='plotly_dark'
    )
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return title, fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
