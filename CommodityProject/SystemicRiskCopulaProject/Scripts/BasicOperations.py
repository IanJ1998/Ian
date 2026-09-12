import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from IPython.display import HTML, display
import plotly.io as pio

def aligning_dataframes(*dfs):
    for df in dfs:
        df["Date"] = pd.to_datetime(df["Date"])

    start_date = max(df["Date"].min() for df in dfs)
    end_date = min(df["Date"].max() for df in dfs)

    return [
        df[df["Date"].between(start_date, end_date)].copy()
        for df in dfs
    ]

def change_dateFormat(df):
    df['Date'] = pd.to_datetime(df['Date'],errors ='coerce').dt.strftime('%Y-%m-%d')

def fillMissingDates(df : pd.DataFrame , date_col : str = "Date", fill_method :str = "ffill", f :str= "D") -> pd.DataFrame:
    """
    Fill missing dates in a DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame with a date column.
    date_col (str): The name of the date column. Default is "Date".
    fill_method (str): The method to fill missing values. Default is "ffill" (forward fill). Possible values are "ffill" (forward fill) and "bfill" (backward fill).
    freq (str): The frequency for the date range. Default is "D" (daily). "B" for business days, "W" for weekly, "M" for monthly, "ME" for month-end, etc.

    Returns:
    pd.DataFrame: A DataFrame with missing dates populated and values .
    """
    # make df sorted n indexed by date
    df.sort_values(date_col,inplace = True)
    try:
        df.set_index(date_col, inplace=True)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        pass

    # generate a complete date range based on the specified frequency and reindex the DataFrame to this range
    full_date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq=f)
    df = df.reindex(full_date_range)

    #Fill method: bfill / ffill .. No interpolate for now--> could be done in future
    if fill_method.lower() == "bfill":
        df_filled = df.bfill().ffill()
    else:
        df_filled = df.ffill().bfill()

    df_filled = df_filled.reset_index(names = date_col)
    return df_filled


def plot_histogram(s: pd.Series, bins: int = 100, ax=None, title: str = ""):
    '''
    s : series or a column squeezed into a series 
    bin: no of bins in histogram
    '''
    s = s.dropna()
    if s.empty:
        return

    mean = s.mean()
    std = s.std(ddof=1)

    if ax is None:
        _, ax = plt.subplots(figsize=(6, 4))

    ax.hist(
        s,
        bins=bins,
        edgecolor='black',
        alpha=0.7,
        color='skyblue',
    )

    ax.axvline(
        mean,
        color='black',
        linestyle='-',
        linewidth=2,
        label=f'Mean ({mean * 100:.2f}%)',
    )

    sigma_colors = {1: 'orange', 2: 'red', 3: 'purple'}
    for i, color in sigma_colors.items():
        pos_val = mean + i * std
        neg_val = mean - i * std
        ax.axvline(
            pos_val,
            color=color,
            linestyle='--',
            linewidth=1.5,
            label=f'+{i}$\\sigma$ ({pos_val * 100:.2f}%)',
        )
        ax.axvline(
            neg_val,
            color=color,
            linestyle='--',
            linewidth=1.5,
            label=f'-{i}$\\sigma$ ({neg_val * 100:.2f}%)',
        )

    ax.set_title(title or 'Histogram of Returns')
    ax.set_xlabel('Return (%)')
    ax.set_ylabel('Frequency')
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.legend(loc='upper right', fontsize=8)

    return ax

def plot_histogram_interactive(
    fig,
    s,
    row,
    col,
    title="",
    bins=100,
    quantiles=(0.01, 0.99),
    ):
    s = pd.to_numeric(s, errors="coerce").dropna()

    if s.empty:
        return

    mean = s.mean()
    std = s.std(ddof=1)

    # Use the central 98% for visual granularity
    lower, upper = s.quantile(quantiles)

    bin_size = (upper - lower) / bins

    fig.add_trace(
        go.Histogram(
            x=s,
            xbins=dict(
                start=lower,
                end=upper,
                size=bin_size,
            ),
            marker_color="skyblue",
            opacity=0.7,
            showlegend=False,
        ),
        row=row,
        col=col,
    )

    fig.add_vline(
        x=mean,
        line_color="black",
        line_width=2,
        annotation_text=f"Mean: {mean * 100:.2f}%",
        row=row,
        col=col,
    )

    for i, color in {1: "orange", 2: "red", 3: "purple"}.items():
        for value in (mean + i * std, mean - i * std):
            fig.add_vline(
                x=value,
                line_color=color,
                line_dash="dash",
                line_width=1.5,
                row=row,
                col=col,
            )

    fig.update_xaxes(
        range=[lower, upper],
        row=row,
        col=col,
    )

def plot_commodity_analysis(dfs: dict, title="Commodity Price and Return Analysis"):
    """
    dfs: dict[str, pd.DataFrame]
        Example:
        {
            "NG": df_ng,
            "Copper": df_cu,
            ...
        }

    Each dataframe must contain:
        - Date
        - Close
        - Relative_change
        - Log_Returns
    """
    if not dfs:
        raise ValueError("dfs must not be empty.")

    nrows = len(dfs)

    fig = make_subplots(
        rows=nrows,
        cols=2,
        specs=[[{"secondary_y": True}, {"secondary_y": False}] for _ in range(nrows)],
        subplot_titles=[
            title_text
            for name in dfs
            for title_text in (
                f"{name}: Relative Change and Log Returns",
                f"{name}: Close Price",
            )
        ],
        horizontal_spacing=0.12,
        vertical_spacing=0.06,
    )

    for row, (name, df) in enumerate(dfs.items(), start=1):
        data = df.copy()
        data["Date"] = pd.to_datetime(data["Date"])
        data = data.dropna(subset=["Date", "Relative_change", "Log_Returns", "Close"]).sort_values("Date")

        # Left panel: Relative change + Log returns
        fig.add_trace(
            go.Scatter(
                x=data["Date"],
                y=data["Relative_change"],
                mode="lines",
                name="Relative Change",
                line=dict(color="royalblue", width=1),
                legendgroup="relative",
                showlegend=row == 1,
            ),
            row=row,
            col=1,
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(
                x=data["Date"],
                y=data["Log_Returns"],
                mode="lines",
                name="Log Returns",
                line=dict(color="firebrick", width=1),
                legendgroup="log",
                showlegend=row == 1,
            ),
            row=row,
            col=1,
            secondary_y=True,
        )

        # Right panel: Close price
        fig.add_trace(
            go.Scatter(
                x=data["Date"],
                y=data["Close"],
                mode="lines",
                name="Close",
                line=dict(color="seagreen", width=1.5),
                legendgroup="close",
                showlegend=row == 1,
            ),
            row=row,
            col=2,
        )

        # Axis labels
        fig.update_yaxes(title_text="Relative Change", row=row, col=1, secondary_y=False)
        fig.update_yaxes(title_text="Log Return", tickformat=".2%", row=row, col=1, secondary_y=True)
        fig.update_yaxes(title_text="Close Price", row=row, col=2)

        fig.update_xaxes(title_text="Date", row=row, col=1)
        fig.update_xaxes(title_text="Date", row=row, col=2)

    fig.update_layout(
        title=title,
        template="plotly_white",
        height=350 * nrows,
        width=1600,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
    )

    return fig

# Stats related

def jarque_bera_test(_df, sk, kurt):
    JB_test = len(_df)/6 * (sk**2 + ((kurt)**2)/4)
    return JB_test


def getBasicStats(df:pd.DataFrame, cols = ['Percentage_Returns', 'Relative_change', 'Log_Returns']):
    stats_dict = {}
    for _y in range(start_date.year, end_date.year+1, 1):
        _ss, _se= pd.Timestamp(_y, 1, 1), pd.Timestamp(_y, 12, 31)
        _start,_end = max(_ss, pd.Timestamp(start_date)),min(_se, pd.Timestamp(end_date))
        df["Date"] = pd.to_datetime(df["Date"])
        _df = df[(df["Date"] >= _start) & (df["Date"] <= _end)].copy()
        sk = _df[cols].skew().rename("skew")
        kurt =_df[cols].kurtosis().rename("kurtosis")
        _jb = jarque_bera_test(_df, sk, kurt).rename("jarque_bera_test")
        stats_dict[_y] = pd.concat([_df[cols].describe().T, sk, kurt, _jb], axis =1)
    return stats_dict