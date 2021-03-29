import pandas as pd
import matplotlib.pyplot as plt

import plotly.figure_factory as ff
import plotly

from sklearn.model_selection import train_test_split


def balance_with_benchmark(df: pd.DataFrame):
    print(
        "For filing date {:.1%} of the reporting periods beat the benchmark".format(
            df["performance_filing"].sum() / df.shape[0]
        )
    )
    print(
        "For earnings date {:.1%} of the reporting periods beat the benchmark".format(
            df["performance_earnings"].sum() / df.shape[0]
        )
    )


def plot_dtribution(
    df: pd.DataFrame, plot_title: str, distro: float = 0.0, title_x: float = 0.28
):
    """Plots the performance distribution for each document as compared to the bechmark.

    Args:
        df (pd.DataFrame): Excepts both the texted and un-texted DataFrames
        plot_title (str): The Name of the plot
        distro (float, optional): When setting to 0.0, this plots all ticker 
        documents in relation to the benchmark. A value of 1 only includes 
        tickers that are both one standard dev above and below
        Defaults to '0.0'.
        title_x (float, optional): because of the skew of the plot, the title 
        may need to be shifted for appearance. Defaults to .28.
    """
    performance_cols = ["performance_earnings_%", "performance_filing_%"]
    performance_labels = ["% Earnings", "% Filing"]

    std = df["performance_filing_%"].describe()["std"]
    sig_df = df[
        (df["performance_filing_%"] >= std * distro)
        | (df["performance_filing_%"] <= -(std * distro))
    ]

    fig = ff.create_distplot(
        [sig_df[c] for c in performance_cols],
        performance_labels,
        bin_size=0.01,
        colors=["#175e54", "#8c1515"],
    )
    fig.update_layout(plot_bgcolor="#f8f6ea")
    fig.update_layout(
        title=plot_title,
        title_x=title_x,
        font=dict(family="Source Sans Pro, bold", size=18, color="#2e2d29"),
    )
    fig.update_layout(
        xaxis_title="% of Benchmark",
        yaxis_title="Number of Company Quarters",
        legend_title="",
        font=dict(family="Source Sans Pro", size=12, color="#2e2d29"),
    )
    fig.add_vrect(x0=0, x1=0, line_color="#2e2d29")
    fig.add_annotation(x=0.1, y=4.5, text="Benchmark", showarrow=False, yshift=0)

    fig.show()


def create_sigma_df(df: pd.DataFrame, z: float = 1.0) -> pd.DataFrame: 
    """Selects only the ticker documents that a z standard deviations above and 
    below the mean.

    Args:
        df (pd.DataFrame): Excepts both the texted and un-texted DataFrames
        z (float, optional): Standard Dev. Defaults to 1.0.

    Returns:
        [type]: [description]
    """
    std = df["performance_filing_%"].describe()["std"]
    one_sig_df = df[
        (df["performance_filing_%"] >= std * z)
        | (df["performance_filing_%"] <= -(std * z))
    ]
    print(
        "Total Number of one sigma tickers: {} or {:.2%} of all the data.".format(
            one_sig_df.shape[0], one_sig_df.shape[0] / df.shape[0]
        )
    )
    return one_sig_df



def split_test_train(df: pd.DataFrame, sigma_df: pd.DataFrame = None, test_size = 0.2, print_=True, seed=1):
    """Test train split based on companies, not individual documents. 

    Args:
        df (pd.DataFrame): [description]
        test_size (float, optional): [description]. Defaults to 0.2.
        print_ (bool, optional): [description]. Defaults to True.

    Returns:
        [type]: Two DataFrames (train and test)
    """    
    all_tickers = df["ticker"].unique()
    ticker_train, ticker_test = train_test_split(all_tickers, test_size=test_size, random_state=seed)
    vlcnt = df["ticker"].value_counts()#.head(80)
    if isinstance(sigma_df, pd.DataFrame) == True:
        print("When Using the Sigma training set, the testing set will be much larger than the implied test_size variable.")
        train_df = sigma_df[sigma_df['ticker'].isin(ticker_train)].copy()
    else:
        train_df = df[df['ticker'].isin(ticker_train)].copy()
    # if sigma_df.empty:
    #     train_df = df[df['ticker'].isin(ticker_train)].copy()
    # else:
    #     print("When Using the Sigma training set, the testing set will be much larger than the implied test_size variable.")
    #     train_df = sigma_df[sigma_df['ticker'].isin(ticker_train)].copy()
    test_df =  df[~df['ticker'].isin(ticker_train)].copy()
    
    if print_ == True:
        print(vlcnt.plot(kind='box', title='Number of Documents Per Company'))
        print(vlcnt.describe())

    actual_size = test_df.shape[0]/train_df.shape[0]
    print("\n\nSince the split is on companies and not documents, the actual document test size is {:.2%}, for a company split of  {:.2%}\nConsider changing the test_size or the seed, which defaults to 1, if concerned.\n\n".format(actual_size,test_size))

    return train_df, test_df
    

if __name__ == "__main__":
    pass
