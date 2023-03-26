#importation des bibliothèques
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table

# Charger les données depuis le fichier CSV
data = pd.read_csv('/home/ec2-user/Linux_Project/data1.csv', names=['price', 'date'])
data['date'] = pd.to_datetime(data['date'])
data['price'] = data['price'].apply(lambda x: float(str(x).replace(" ", "")))

table_data = [
    {'Volatility': 0.05, 'Open Price': 100, 'Close Price': 110},
]# valeurs fictives et mise à jour plus tard des réelles valeurs

#création d'une instance de l'application Dash
app = dash.Dash(__name__)

#définition de la strcuture du dashboard
app.layout = html.Div(
    style={'backgroundColor': '#F2F2F2'},
    children=[        
        html.H1('Financial Website', style={'textAlign': 'center', 'color': 'black'}),
        # ajout de la série temporelle ( Prix en fonction de la date)       
        dcc.Graph(            
            id='price-graph',            
            figure={                
                'data': [                    
                    {'x': data['date'], 'y': data['price'], 'type': 'line', 'name': 'Price', 'line': {'color': 'orange'}}
                ],
                'layout': {
                    'title': 'S&P 500',
                    'xaxis': {'title': 'Date'},
                    'yaxis': {'title': 'Price'},
                    'plot_bgcolor': '#F2F2F2',
                    'paper_bgcolor': '#F2F2F2',
                }
            }
        ),
        #intervalle de temps pour mettre à jour la série temporelles toutes les 5 minutes
        dcc.Interval(
            id='interval-component',
            interval=5*60*1000, # toutes les 5 minutes
            n_intervals=0
        ),
        # ajout du tableau qui affiche des metrics ( 3 metrics: volatilite, open price, closed price)
        dash_table.DataTable(
            id='price-table',
            columns=[{'name': col, 'id': col} for col in table_data[0].keys()],
            data=table_data
        ),
        #intervale pour mettre à jour le tableau une fois par jour
        dcc.Interval(
            id='interval-daily',
            interval=60*60*1000,  # toutes les heures
            n_intervals=0
        )
    ]
)


# Callback pour la mise à jour des données toutes les 5 minutes
@app.callback(
    dash.dependencies.Output('price-graph', 'figure'),
    dash.dependencies.Input('interval-component', 'n_intervals'))
def update_graph(n):
    global data
    data = pd.read_csv('/home/ec2-user/Linux_Project/data1.csv', names=['price', 'date'])
    data['date'] = pd.to_datetime(data['date'])
    data['price'] = data['price'].apply(lambda x: float(str(x).replace(" ", "")))
    return {'data': [{'x': data['date'], 'y': data['price'], 'type': 'line', 'name': 'Price', 'line': {'color': 'orange'}}],
            'layout': {'title': 'S&P 500', 'xaxis': {'title': 'Date'}, 'yaxis': {'title': 'Price'},
                       'plot_bgcolor': '#F2F2F2', 'paper_bgcolor': '#F2F2F2'}}

@app.callback(
    dash.dependencies.Output('price-table', 'data'),
    dash.dependencies.Input('interval-daily', 'n_intervals'))
def update_table(n):
    # Définir l'heure de la mise à jour quotidienne
    global data
    update_time = pd.datetime.now().replace(hour=20, minute=00, second=0, microsecond=0)
    if pd.datetime.now() < update_time:
        # Si l'heure actuelle est avant l'heure de mise à jour, ne rien faire
        return dash.no_update
    else:
        # Sinon, calculer les nouvelles données
        today = pd.Timestamp.today()
        today_start = pd.datetime(today.year, today.month, today.day, 9, 0, 0)#ouverture de la bourse
        today_end = pd.datetime(today.year, today.month, today.day, 17, 30, 0)#fermeture de la bourse
        today_data = data.loc[(data['date'] >= today_start) & (data['date'] <= today_end)]

        # Calculer les metrics pour la journée
        open_price = today_data['price'].iloc[0]
        close_price = today_data['price'].iloc[-1]
        volatility = round((close_price - open_price) / open_price * 100, 2)

        # Mettre à jour les données du tableau
        new_data = [{'Volatility': volatility, 'Open Price': open_price, 'Close Price': close_price}]
        return new_data

#démarrer le serveur de l'application
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8050, debug= True)



