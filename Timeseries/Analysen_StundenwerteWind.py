"""This script analysis hourly wind data as retrieved from
https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate
/hourly/wind/historical/

"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import date
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

def read_data(file):
    """

    :param file: str of path to file
    :return:
    """
    filepath = Path(file)
    df = pd.read_csv(filepath, sep=";")
    df.loc[:, "MESS_DATUM"] = pd.to_datetime(df.loc[:, "MESS_DATUM"],
                                             format="%Y%m%d%H")
    df.set_index("MESS_DATUM", inplace=True)
    df = df.loc[df["   F"] >= 0]  # remove outliers / negative windspeeds

    return df


def annual_cycle(df):
    """ Returns dataframe with annual cycle.
    ! Dataframe needs to have a timebased index !

    :param df:
    :return:
    """
    df = df.groupby([df.index.month, df.index.day]).mean()
    return df


def wind_scatterplot(df, path):
    """

    :param df: pandas.core.frame.DataFrame
    :return:
    """
    savefigto = Path(path).parent
    fig, ax = plt.subplots()
    ax.scatter(x=df.index.values, y=df["   F"])
    plt.tight_layout()
    fig.savefig(savefigto, dpi=500)
    fig.show()


def plot_annual_cycle(ser, path, plot_current_date=False):
    """

    :param ser: pandas.core.series.Series
    :return:
    """
    timeline = pd.date_range("2020-01-01", "2020-12-31")
    savefigto = Path(path).parent

    if plot_current_date:
        current_day = date.today().day
        current_month = date.today().month
        today = pd.to_datetime(
            "2020-" + str(current_month) + "-" + str(current_day))

    fig, ax = plt.subplots()
    ax.plot(timeline, ser.rolling(window=14, center=True).mean().values,
            c='k', label="Daily average windspeed, 14 day rolling mean")
    ax.xaxis.set_major_formatter(DateFormatter("%b"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    if plot_current_date:
        ax.axvline(today, c='r', ls='--', label="Current day")
    ax.legend()
    ax.set_xlim(left=pd.to_datetime("2020-01-01"),
                right=pd.to_datetime("2020-12-31"))
    ax.set(ylabel="Average daily windspeed [m/s]", xlabel="Month")
    ax.grid()
    fig.savefig(savefigto, dpi=500)
    fig.show()


if __name__ == "__main__":
    path = (r"C:\Users\sb123\Desktop\Klima\observations_germany"
            r"\Gluecksburg"
            r"\stundenwerte_FF_01666_19710101_20071231_hist"
            r"\produkt_ff_stunde_19710101_20071231_01666.txt")
    wind = read_data(path)
    # wind_scatterplot(wind, path)
    wind_annual = annual_cycle(wind.loc[:, "   F"])
    plot_annual_cycle(wind_annual, path)