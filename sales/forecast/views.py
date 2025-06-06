from django.shortcuts import render
from .utils import predict_sales
from database.models import Stores, Products
import tempfile
import os
import pandas as pd
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def forecast_page(request):
    chart_data = None
    error_msg = None
    tmp_path = None

    stores = Stores.objects.all()
    products = Products.objects.all()

    if request.method == 'POST' and request.FILES.get('data_file'):
        try:
            period = int(request.POST.get('period', 14))
            store_id = request.POST.get('store_id')
            product_id = request.POST.get('product_id')

            if not store_id or not product_id:
                raise ValueError("Не выбраны магазин и/или товар.")

            data_file = request.FILES['data_file']

            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
                for chunk in data_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            df_result = predict_sales(
                file_path=tmp_path,
                period_days=period,
                store_id=store_id,
                product_id=product_id
            )

            if not df_result.empty:
                df_result['date'] = pd.to_datetime(df_result['date']).astype(str)
                chart_data = df_result[['date', 'predicted']].to_dict(orient='records')
            else:
                error_msg = 'Нет данных для выбранной связки магазин + товар.'

        except Exception as ex:
            error_msg = f'Ошибка: {str(ex)}'
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

    return render(request, 'forecast/forecast_page.html', {
        'chart_data': chart_data,
        'error_msg': error_msg,
        'stores': stores,
        'products': products
    })
