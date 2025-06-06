from django.db import models

class Stores(models.Model):
    STORE_FORMAT_CHOICES = [
        ('ГП', 'ГП'),
        ('СМ', 'СМ'),
    ]

    store_id = models.CharField('Код магазина', max_length=50, primary_key=True)
    short_name = models.CharField('Краткое наименование', max_length=100)
    cluster = models.CharField('Округ', max_length=50)
    region = models.CharField('Регион', max_length=50)
    store_format = models.CharField(
        max_length=2,
        choices=STORE_FORMAT_CHOICES,
        verbose_name="Формат склада"
    )
    begin_date = models.DateField('Дата открытия')

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

class Products(models.Model):
    product_id = models.CharField('Код товара', max_length=50, primary_key=True)
    category = models.CharField('Категория', max_length=100)
    name = models.CharField('Название', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class Promo(models.Model):
    promo_id = models.CharField('Код акции', max_length=50, primary_key=True)
    type = models.CharField('Тип акции', max_length=100)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Промо-акция'
        verbose_name_plural = 'Промо-акции'


class Sales(models.Model):
    date = models.DateField('Дата')
    store = models.ForeignKey(Stores, to_field='store_id', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, to_field='product_id', on_delete=models.CASCADE)
    promo = models.ForeignKey(Promo, to_field='promo_id', on_delete=models.CASCADE, blank=True, null=True)
    sales = models.FloatField('Количество')

    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'
        constraints = [
            models.UniqueConstraint(fields=['date', 'store', 'product', 'promo'], name='unique_sale_entry')
        ]

    def __str__(self):
        return f"{self.date} | {self.store_id} | {self.product_id} | {self.promo_id}"