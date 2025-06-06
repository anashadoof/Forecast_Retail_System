import pandas as pd
from sales.database.models import Stores, Products, Promo, Sales
from django.utils.dateparse import parse_date

df = pd.read_csv('C:/Users/dns/Desktop/диплом/df_cleaned_2.csv')

def clean_id(val):
    try:
        if pd.isna(val):
            return ''
        val = str(val)
        if val.endswith('.0'):
            val = val[:-2]
        return val
    except Exception:
        return str(val)

df['store_id'] = df['store_id'].astype(str).str.strip()
df['product_id'] = df['product_id'].astype(str).str.strip()
df['promo_id'] = df['promo_id'].apply(clean_id)

for i, row in df.iterrows():
    store_id = row['store_id']
    product_id = row['product_id']
    promo_id = row['promo_id']
    date = row['date'][:10]

    if not (store_id and product_id and promo_id):
        print(f"Skip row: store_id={store_id}, product_id={product_id}, promo_id={promo_id}")
        continue

    # Проверка на существование (чтобы не было foreign key ошибки)
    if not Stores.objects.filter(store_id=store_id).exists():
        print(f"Skip row, store not found: {store_id}")
        continue
    if not Products.objects.filter(product_id=product_id).exists():
        print(f"Skip row, product not found: {product_id}")
        continue
    if not Promo.objects.filter(promo_id=promo_id).exists():
        print(f"Skip row, promo not found: {promo_id}")
        continue

    store = Stores.objects.get(store_id=store_id)
    product = Products.objects.get(product_id=product_id)
    promo = Promo.objects.get(promo_id=promo_id)

    Sales.objects.create(
        date=parse_date(date),
        store=store,
        product=product,
        promo=promo,
        sales=row['sales']
    )
