from database.models import Stores
from datetime import datetime
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Загрузка магазинов'

    def handle(self, *args, **options):
        store_data = [
            {
                'short_name': 'Гипермаркет Краснодар-3',
                'cluster': 'Южный',
                'region': 'Краснодарский край',
                'store_format': 'ГП',
                'begin_date': '2018-03-15',
                'end_date': 'Открыт'
            },
            {
                'short_name': 'Супермаркет Краснодар-5',
                'cluster': 'Южный',
                'region': 'Краснодарский край',
                'store_format': 'СМ',
                'begin_date': '2019-07-10',
                'end_date': 'Открыт'
            },
            {
                'short_name': 'Гипермаркет Воронеж-1',
                'cluster': 'Центральный',
                'region': 'Воронежская область',
                'store_format': 'ГП',
                'begin_date': '2020-05-21',
                'end_date': 'Открыт'
            },
            {
                'short_name': 'Супермаркет Ростов-1',
                'cluster': 'Южный',
                'region': 'Ростовская область',
                'store_format': 'СМ',
                'begin_date': '2021-09-17',
                'end_date': 'Открыт'
            },
            {
                'short_name': 'Гипермаркет Екатеринбург-1',
                'cluster': 'Уральский',
                'region': 'Свердловская область',
                'store_format': 'ГП',
                'begin_date': '2017-11-04',
                'end_date': 'Открыт'
            },
            {
                'short_name': 'Супермаркет Москва-4',
                'cluster': 'Центральный',
                'region': 'Москва',
                'store_format': 'СМ',
                'begin_date': '2019-04-23',
                'end_date': 'Открыт'
            },
            {
                'short_name': 'Гипермаркет Москва-7',
                'cluster': 'Центральный',
                'region': 'Москва',
                'store_format': 'ГП',
                'begin_date': '2023-01-12',
                'end_date': 'Открыт'
            },
            {
                'short_name': 'Супермаркет Петербург-4',
                'cluster': 'Северо-Западный',
                'region': 'Санкт-Петербург',
                'store_format': 'СМ',
                'begin_date': '2018-10-27',
                'end_date': 'Открыт'
            },
            {
                'short_name': 'Гипермаркет Петербург-19',
                'cluster': 'Северо-Западный',
                'region': 'Санкт-Петербург',
                'store_format': 'ГП',
                'begin_date': '2020-12-14',
                'end_date': 'Открыт'
            },
            {
                'short_name': 'Супермаркет Петербург-23',
                'cluster': 'Северо-Западный',
                'region': 'Санкт-Петербург',
                'store_format': 'СМ',
                'begin_date': '2022-03-05',
                'end_date': 'Открыт'
            },
        ]

        for item in store_data:
            Stores.objects.create(
                short_name=item['short_name'],
                cluster=item['cluster'],
                region=item['region'],
                store_format=item['store_format'],
                begin_date=datetime.strptime(item['begin_date'], "%Y-%m-%d"),
                end_date=item['end_date']
            )
        self.stdout.write(self.style.SUCCESS('Данные успешно добавлены!'))
