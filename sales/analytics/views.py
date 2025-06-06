from django.shortcuts import render
from django.http import JsonResponse
from database.models import Stores, Products, Sales
import pandas as pd
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def analytics_dashboard(request):
    stores = Stores.objects.all()
    products = Products.objects.all()
    return render(request, "analytics/dashboard.html", {
        "stores": stores,
        "products": products,
    })

def get_chart_data(request):
    chart_type = request.GET.get('chart_type')
    store_id = request.GET.get('store_id')
    product_id = request.GET.get('product_id')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    qs = Sales.objects.all()
    if store_id and store_id != 'all':
        qs = qs.filter(store__store_id=store_id)
    if product_id and product_id != 'all':
        qs = qs.filter(product__product_id=product_id)
    if date_from:
        qs = qs.filter(date__gte=date_from)
    if date_to:
        qs = qs.filter(date__lte=date_to)

    df = pd.DataFrame(list(qs.values('date', 'sales', 'store__store_id', 'product__product_id', 'product__name')))
    if df.empty or len(df) < 5:
        return JsonResponse({'status': 'error', 'msg': 'Нет или недостаточно данных для выбранных фильтров'})

    # 1. Распределение продаж по периоду (line)
    if chart_type == 'sales_distribution':
        df_grouped = df.groupby('date').sales.sum().reset_index()
        # Оценка востребованности
        if store_id and store_id != 'all' and product_id and product_id != 'all':
            # Забираем продажи ВСЕХ товаров в этом магазине за тот же период
            store_qs = Sales.objects.filter(store__store_id=store_id)
            if date_from:
                store_qs = store_qs.filter(date__gte=date_from)
            if date_to:
                store_qs = store_qs.filter(date__lte=date_to)
            df_store = pd.DataFrame(list(store_qs.values('sales', 'product__product_id')))

            total_store_sales = df_store['sales'].sum()
            product_sales = df['sales'].sum()
            demand_share = (product_sales / total_store_sales) * 100 if total_store_sales > 0 else 0
            info_text = f"Востребованность товара в этом магазине: {demand_share:.1f}% от всех продаж"
        else:
            info_text = "Выберите конкретный магазин и товар для оценки востребованности"
        return JsonResponse({
            'status': 'ok',
            'plot': {
                'x': df_grouped['date'].astype(str).tolist(),
                'y': df_grouped['sales'].tolist(),
                'type': 'scatter',
                'mode': 'lines+markers',
                'line': {'color': '#4991FF'}
            },
            'layout': {
                'margin': {'t': 48},
                'font': {'family': "Arial, Verdana, sans-serif"},
                'xaxis': {'title': 'Дата'},
                'yaxis': {'title': 'Продажи'},
            },
            'info': info_text
        })

    # 2. ТОП-3 товаров по продажам для магазина (bar)
    elif chart_type == 'top_products':
        if store_id and store_id != 'all':
            # Группируем по product__product_id и product__name (имя товара)
            df_top = (
                df.groupby(['product__product_id', 'product__name'])
                    .sales.sum()
                    .sort_values(ascending=False)
                    .head(3)
                    .reset_index()
            )
            return JsonResponse({
                'status': 'ok',
                'plot': {
                    'x': df_top['product__name'].tolist(),
                    'y': df_top['sales'].tolist(),
                    'type': 'bar',
                    'marker': {'color': '7862FF'}
                },
                'layout': {
                    # 'title': 'ТОП-3 товаров по продажам',
                    'margin': {'t': 48},
                    'font': {'family': "Arial, Verdana, sans-serif"},
                    'xaxis': {'title': 'Товар'},
                    'yaxis': {'title': 'Продажи'},
                },
                # 'info': ''
            })
        else:
            return JsonResponse({'status': 'error', 'msg': 'Выберите магазин!'})


    # 3. Распределение по месяцам (bar + линия)
    elif chart_type == 'monthly_sales':
        df['month'] = pd.to_datetime(df['date']).dt.month
        df_month = df.groupby('month').sales.sum().reset_index()
        return JsonResponse({
            'status': 'ok',
            'plot': {
                'x': df_month['month'].tolist(),
                'y': df_month['sales'].tolist(),
                'type': 'bar',
                'marker': {'color': '#00AE6F'}
            },
            'layout': {
                'margin': {'t': 48},
                'font': {'family': "Arial, Verdana, sans-serif"},
                'xaxis': {'title': 'Месяц', 'tickmode': 'array', 'tickvals': list(range(1,13)),
                          'ticktext': ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']},
                'yaxis': {'title': 'Продажи'},
            }
        })

    # 4. Распределение по дням недели (bar)
    elif chart_type == 'weekday_sales':
        df['weekday'] = pd.to_datetime(df['date']).dt.dayofweek
        days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        df_wd = df.groupby('weekday').sales.sum().reindex(range(7), fill_value=0).reset_index()
        return JsonResponse({
            'status': 'ok',
            'plot': {
                'x': [days[x] for x in df_wd['weekday']],
                'y': df_wd['sales'].tolist(),
                'type': 'bar',
                'marker': {'color': '#FE5B5C'}
            },
            'layout': {
                'margin': {'t': 48},
                'font': {'family': "Arial, Verdana, sans-serif"},
                'xaxis': {'title': 'День недели'},
                'yaxis': {'title': 'Продажи'},
            }
        })

    return JsonResponse({'status': 'error', 'msg': 'Неизвестный тип графика'})
