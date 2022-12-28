import pandas as pd
from cachetools import TTLCache, cached
from django.db import transaction

from rechner.models import Month


def _remove_chars(column, chars):
    for char in chars:
        column = column.str.replace(char, '', regex=False)

    return column


@transaction.atomic()
def update_price_db():
    Month.objects.all().delete()

    df_base_index = fetch_base_index()
    df_hypo = fetch_hypo()

    months = []

    for _, row in df_base_index.iterrows():
        date = row['date']
        months.append(
            Month(
                month=row['date'],
                base_index=row['1982'],
                hypo=get_hypo_for_date(df_hypo, date),
            ))

    Month.objects.bulk_create(months)


def fetch_base_index():
    url = 'https://dam-api.bfs.admin.ch/hub/api/dam/assets/23772749/master'
    base_index = pd.read_excel(url, skiprows=3, skipfooter=1)
    base_index.columns = pd.Index(
        ['date'] + pd.DatetimeIndex(base_index.columns[1:-2]).to_period('Y').astype(str).to_list() +
        base_index.columns[-2:].to_list())
    return base_index[['date', '1982']].dropna()


@cached(cache=TTLCache(maxsize=5, ttl=60))
def fetch_hypo():
    hypo = pd.read_html(
        'https://www.bwo.admin.ch/bwo/de/home/mietrecht/referenzzinssatz/entwicklung-referenzzinssatz-und-durchschnittszinssatz.html'
    )[0]

    hypo['hypo_value'] = pd.to_numeric(
        _remove_chars(
            hypo['Hypothekarischer Referenzzinssatz  bei Mietverhältnissen'],
            '%* ',
        ).str.strip().str.replace(',', '.'),
        errors='coerce',
    )
    hypo['date'] = pd.to_datetime(hypo['gültig ab'], dayfirst=True, errors='coerce')

    return hypo[['date', 'hypo_value']].dropna().sort_values('date')


def get_hypo_for_date(df_hypo, date) -> float:
    idx = df_hypo['date'].searchsorted(date)

    if idx > 0:
        return df_hypo.iloc[idx - 1].hypo_value

    return df_hypo.iloc[idx].hypo_value
