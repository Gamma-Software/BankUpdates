import pandas as pd
import plotly
import plotly.graph_objects as go
from getAccounts.excel_interface import ExcelInterface


def show_balance(df: pd.DataFrame, options):
    print("Show balance")
    nb_items = df.shape[1]

    # Create the figure
    fig = go.Figure()

    # Display the evolution
    for i in range(1, nb_items):
        print(df['timestamp'])
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df.iloc[:, i], name=df.iloc[:, i].name, line_shape=options['line_shape']),
            row=i, col=1)

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            linecolor='rgb(204, 204, 204)',
            linewidth=1,
            ticks='outside'
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
        ),
        showlegend=False,
        plot_bgcolor='white',
    )

    fig.update_xaxes(
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


if __name__ == "__main__":
    excel_interface = ExcelInterface('accounts.xlsx')

    # execute only if run as a script
    accounts = excel_interface.read_excel_in_pd()
    if not accounts.empty:
        show_balance(accounts, {'line_shape': 'spline'})
