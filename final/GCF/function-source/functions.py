import datetime
import pandas as pd
import requests
from google.cloud import secretmanager
import os

APP_NAME = 'mobkoiTask'
ACCESS_TOKEN = os.environ.get('SECRETKEY')
WIKI_API = "https://en.wikipedia.org/w/api.php"

pd.options.mode.chained_assignment = None  # default='warn'


def get_page_views(date,access,app):
    """
    Get page view data from the Wikimedia REST API.

    This function queries the Wikimedia REST API for the top viewed pages 
    on a particular date.

    Parameters
    ----------
    date : str
        A string representation of the date in format 'YYYY/MM/DD'.

    Returns
    -------
    df : pandas.DataFrame
        A dataframe containing page view data for the provided date.
    """
    date = pd.to_datetime(date).strftime('%Y/%m/%d')
    PAGE_VIEW_API = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia.org/all-access/{date}"
    headers = {
        'Authorization': f'Bearer {access}',
        'User-Agent': f'{app}'
    }
    url = PAGE_VIEW_API
    response = requests.get(url, headers=headers)
    data = response.json()

    # convert data to dataframe
    df = pd.json_normalize(data['items'][0]['articles'])
    df['date'] = date  # add the date column to the dataframe

    return df

def get_dates(from_date, to_date):
    """
    Generate a list of dates between from_date and to_date.

    This function generates a list of dates from the start date (from_date) 
    to the end date (to_date). If both from_date and to_date are None, 
    it returns the current date. If only from_date is provided, the range 
    will be from the provided date to itself, thus returning a list with a single date.
    If only to_date is provided, the range will be from the provided date to itself, 
    thus returning a list with a single date.

    Parameters
    ----------
    from_date : str or None
        A string representation of the start date in format 'YYYY-MM-DD'. 
        If None and to_date is not provided, it's set to the current date.
        If None and to_date is provided, it's set to the value of to_date.
    to_date : str or None
        A string representation of the end date in format 'YYYY-MM-DD'. 
        If None and from_date is not provided, it's set to the current date.
        If None and from_date is provided, it's set to the value of from_date.

    Returns
    -------
    list
        A list of dates in string format.

    Raises
    ------
    ValueError
        If from_date is later than to_date.
    """
    if from_date is None and to_date is None:
        from_date = to_date = datetime.datetime.now().strftime('%Y-%m-%d')
    elif from_date is None:
        from_date = datetime.datetime.now().strftime('%Y-%m-%d')
    elif to_date is None:
        to_date = datetime.datetime.now().strftime('%Y-%m-%d')
    else:
        from_date = pd.to_datetime(from_date)
        to_date = pd.to_datetime(to_date)

    if from_date > to_date:
        raise ValueError("from_date cannot be later than to_date")

    return pd.date_range(from_date, to_date).strftime('%Y-%m-%d').tolist()


def process_dates(from_date=None, to_date=None):
    """
    Process a range of dates to get page view data.

    This function processes a range of dates and calls the get_page_views function 
    for each date to get the page view data for that date.

    Parameters
    ----------
    from_date : str or None
        A string representation of the start date in format 'YYYY-MM-DD'. 
        If None, it's set to the current date.
    to_date : str or None
        A string representation of the end date in format 'YYYY-MM-DD'. 
        If None, it's set to the current date.

    Returns
    -------
    all_data_df : pandas.DataFrame
        A dataframe containing page view data for all dates.
    """
    dates = get_dates(from_date, to_date)
    all_data = []
    for date in dates:
        data = get_page_views(date,access=ACCESS_TOKEN,app=APP_NAME)
        all_data.append(data)
    all_data_df = pd.concat(all_data, ignore_index=True)
    return all_data_df

def get_categories(page_title):
    """
    Get categories for a Wikipedia page.

    This function gets the categories for a particular Wikipedia page by querying 
    the Wikipedia API.

    Parameters
    ----------
    page_title : str
        The title of the Wikipedia page.

    Returns
    -------
    categories : list
        A list of categories for the Wikipedia page.
    """
    session = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json",
        "prop": "categories",
        "titles": page_title
    }
    request = session.get(url=URL, params=PARAMS)
    DATA = request.json()

    PAGES = DATA["query"]["pages"]
    categories = []
    for k, v in PAGES.items():
        if 'categories' in v:
            for cat in v['categories']:
                categories.append(cat["title"][9:])
    return categories

def process_dataframe(data):
    """
    Process a dataframe to get categories for each article.

    This function processes a dataframe containing page view data and appends a new column 
    with the categories for each article.

    Parameters
    ----------
    data : pandas.DataFrame
        A dataframe containing page view data.

    Returns
    -------
    data : pandas.DataFrame
        A dataframe containing page view data along with the categories for each article.
    """
    data['article_categories'] = data['article'].apply(get_categories)
    data = data.explode(column="article_categories")
    data = data[['date','article','article_categories', 'rank','views']]
    return data

def main_process(from_date, to_date):
    """
    Main processing function to get the final dataframe.

    This function is a pipeline function that first gets the page view data for a range of 
    dates, then filters out rows with rank greater than 100, and finally processes the dataframe 
    to get categories for each article.

    Parameters
    ----------
    from_date : str
        A string representation of the start date in format 'YYYY-MM-DD'.
    to_date : str
        A string representation of the end date in format 'YYYY-MM-DD'.

    Returns
    -------
    final : pandas.DataFrame
        A dataframe containing page view data along with the categories for each article.
    """
    data = process_dates(from_date=from_date, to_date=to_date)
    data = data[data['rank'] <= 100]
    final = process_dataframe(data)
    return final
