import pandas as pd
import plotly
import plotly.graph_objects as go
from get_account_api.excel_interface import ExcelInterface
import path_files
from scipy.signal import find_peaks


def plot(df: pd.DataFrame, options):
    print("Show balance")

    # Create the figure
    fig = go.Figure()

    # List the buttons settings
    button_list = list()
    indices = []

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
                       visible=True if i == 1 else False))
        fig.add_trace(
            go.Scatter(
                x=[df['timestamp'][j] for j in find_peaks(df.iloc[:, i])[0]],
                y=[df.iloc[:, i][j] for j in find_peaks(df.iloc[:, i])[0]],
                mode='markers',
                marker=dict(
                    size=8,
                    color='red',
                    symbol='cross'
                ),
                name='Detected Peaks',
                visible=True if i == 1 else False))

        # Add button settings
        button_list.append(
            dict(label=name,
                 method="update",
                 args=[{"visible": [[o == i, o == i][1:-1] for o in range(1, nb_items*2, 1)]},
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
    plotly.offline.plot(fig, filename='account.html')


def show_balance():
    excel_interface = ExcelInterface(path_files.data_temp_file, path_files.account_filename)

    # execute only if run as a script
    accounts = excel_interface.read_excel_in_pd()
    if not accounts.empty:
        plot(accounts, {'line_shape': 'spline', 'color': 'rgb(0, 143, 213)'})


if __name__ == "__main__":
    show_balance()
