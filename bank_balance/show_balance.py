import pandas as pd
import plotly
import plotly.graph_objects as go
from bank_balance.library.excelinterface import ExcelInterface
import bank_balance.library.parametersparsing as conf
from bank_balance.library import pathfiles
import os


def plot(df: pd.DataFrame, options):
    print("Show balance")

    # Create the figure
    fig = go.Figure()

    # List the buttons settings
    button_list = list()

    # Loop over the account balance
    nb_items = df.shape[1]
    for i in range(1, nb_items):
        name = df.iloc[:, i].name

        # Add account balance trace
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df.iloc[:, i],
                       name=name,
                       hovertemplate='Balance: %{y:.2f}€<extra></extra>',
                       line_shape=options['line_shape'],
                       line=dict(color="rgb(0, 143, 213)", width=3, dash="dot"),
                       marker=dict(size=8),
                       y_range=(0, df.iloc[:, i]),
                       visible=True if i == 1 else False))

        # Add button settings
        button_list.append(
            dict(label=name,
                 method="update",
                 args=[{"visible": [o == i for o in range(nb_items)]},
                       {"title": "<b>"+name+"</b>",
                        "annotations": []}]))

    # Update layout (color, legend, button)
    fig.update_layout(
        margin=dict(t=150, b=20),
        showlegend=False,
        plot_bgcolor='rgb(230, 230,230)',
        paper_bgcolor='rgb(240,240,240)',
        updatemenus=[
            dict(
                type="buttons",
                direction="down",
                buttons=button_list,
                active=0,
            )
        ],
        xaxis_title='date',
        yaxis_title='balance',
        title="<b>"+df.iloc[:, 1].name+"</b>",
        title_x=0.5,
        font=dict(
            size=16,
            color="rgb(68,68,68)"
        ),
        hovermode='x unified'
    )

    # Add picker date and range slider
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    fig.show()

    options = conf.parse_setup_options(pathfiles.setup_options)
    path = pathfiles.temp_folder
    if options['save'] == 'local':
        if options['local_path'] != 'none':
            path = options['local_path']
    plotly.offline.plot(fig, filename=os.path.join(path, 'account.html'))
    print('save in ' + os.path.join(path, 'account.html'))

def show_balance():
    # Read options
    options = conf.parse_setup_options(pathfiles.setup_options)
    path = pathfiles.temp_folder
    if options['save'] == 'local':
        if options['local_path'] != 'none':
            path = options['local_path']
    print('1')
    excel_interface = ExcelInterface(path, pathfiles.account_filename)
    print('2')
    # execute only if run as a script
    accounts = excel_interface.read_excel_in_pd()
    if not accounts.empty:
        plot(accounts, {'line_shape': 'linear', 'color': 'rgb(0, 143, 213)'})
    else:
        print('nothing to plot')

if __name__ == "__main__":
    show_balance()
