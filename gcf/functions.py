import datetime
import pandas as pd
import requests
from vars import ACCESS_TOKEN, APP_NAME

pd.options.mode.chained_assignment = None  # default='warn'


def get_page_views(date):
    date = pd.to_datetime(date).strftime('%Y/%m/%d')
    PAGE_VIEW_API = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia.org/all-access/{date}"
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'User-Agent': f'{APP_NAME}'
    }
    url = PAGE_VIEW_API
    response = requests.get(url, headers=headers)
    data = response.json()

    # convert data to dataframe
    df = pd.json_normalize(data['items'][0]['articles'])
    df['date'] = date  # add the date column to the dataframe

    return df

def get_dates(from_date, to_date):
    if from_date is None and to_date is None:
        from_date = to_date = datetime.datetime.now().strftime('%Y-%m-%d')
    elif from_date is None:
        from_date = to_date
    else:
        from_date = pd.to_datetime(from_date)
        to_date = pd.to_datetime(to_date)

    if from_date > to_date:
        raise ValueError("from_date cannot be later than to_date")

    return pd.date_range(from_date, to_date).strftime('%Y-%m-%d').tolist()

def process_dates(from_date=None, to_date=None):
    dates = get_dates(from_date, to_date)
    all_data = []
    for date in dates:
        data = get_page_views(date)
        all_data.append(data)
    all_data_df = pd.concat(all_data, ignore_index=True)
    return all_data_df

def get_categories(page_title):
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
    data['article_categories'] = data['article'].apply(get_categories)
    data = data.explode(column="article_categories")
    dataddataf = data[['date','article','article_categories', 'rank','views']]
    return data

def main_process(from_date, to_date):
    data = process_dates(from_date=from_date, to_date=to_date)
    data = data[data['rank'] <= 100]
    final = process_dataframe(data)
    return final


# main_process(from_date='2023-04-02',to_date='2023-04-03')
# main_process(from_date='2023-04-01',to_date='2023-04-05')