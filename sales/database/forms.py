from django import forms
from .models import Stores, Products, Promo, Sales

class StoreForm(forms.ModelForm):
    class Meta:
        model = Stores
        fields = ['store_id', 'short_name', 'cluster', 'region', 'store_format', 'begin_date']
        widgets = {
            'store_id': forms.TextInput(attrs={'class': 'form-control form-field', 'placeholder': 'Введите код магазина'}),
            'short_name': forms.TextInput(
                attrs={'class': 'form-control form-field only-letters', 'placeholder': 'Введите наименование'}),
            'cluster': forms.TextInput(
                attrs={'class': 'form-control form-field only-letters', 'placeholder': 'Введите округ'}),
            'region': forms.TextInput(
                attrs={'class': 'form-control form-field only-letters', 'placeholder': 'Введите регион'}),
            'store_format': forms.Select(attrs={'class': 'form-control form-field'}),
            'begin_date': forms.DateInput(attrs={'class': 'form-control form-field', 'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        is_edit = kwargs.pop('is_edit', False)
        super().__init__(*args, **kwargs)

        if is_edit:
            self.fields['store_id'].disabled = True

        for field in self.fields.values():
            field.required = True

        self.fields['store_format'].required = True
        self.fields['begin_date'].input_formats = ['%Y-%m-%d']

    def clean_store_id(self):
        store_id = self.cleaned_data.get('store_id')
        if self.instance.pk is None:
            if Stores.objects.filter(store_id=store_id).exists():
                raise forms.ValidationError('Магазин с таким кодом уже существует!')
        return store_id


class ProductForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = ['product_id', 'category', 'name']
        widgets = {
            'product_id': forms.TextInput(attrs={
                'class': 'form-control form-field only-digits',
                'placeholder': 'Введите код (только цифры)'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control form-field only-letters',
                'placeholder': 'Введите категорию'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control form-field upper-case',
                'placeholder': 'Введите наименование'
            }),
        }

    def __init__(self, *args, **kwargs):
        is_edit = kwargs.pop('is_edit', False)
        super().__init__(*args, **kwargs)

        if is_edit:
            self.fields['product_id'].disabled = True

        for field in self.fields.values():
            field.required = True

    def clean_product_id(self):
        product_id = self.cleaned_data['product_id']
        if self.instance.pk is None:
            if Products.objects.filter(product_id=product_id).exists():
                raise forms.ValidationError('Товар с таким кодом уже существует!')
        return product_id


class PromoForm(forms.ModelForm):
    class Meta:
        model = Promo
        fields = ['promo_id', 'type']
        widgets = {
            'promo_id': forms.TextInput(attrs={'class': 'form-control form-field only-digits', 'placeholder': 'Введите код акции'}),
            'type': forms.TextInput(attrs={'class': 'form-control form-field upper-case', 'placeholder': 'Введите тип акции'})
        }

    def __init__(self, *args, **kwargs):
        is_edit = kwargs.pop('is_edit', False)
        super().__init__(*args, **kwargs)

        if is_edit:
            self.fields['promo_id'].disabled = True

        for field in self.fields.values():
            field.required = True

    def clean_promo_id(self):
        promo_id = self.cleaned_data['promo_id']
        if self.instance.pk is None:
            if Promo.objects.filter(promo_id=promo_id).exists():
                raise forms.ValidationError('Промо-акция с таким кодом уже существует!')
        return promo_id

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['date', 'store', 'product', 'promo', 'sales']
        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control form-field'}),
            'store': forms.Select(attrs={'class': 'form-control form-field'}),
            'product': forms.Select(attrs={'class': 'form-control form-field'}),
            'promo': forms.Select(attrs={'class': 'form-control form-field'}),
            'sales': forms.NumberInput(attrs={'class': 'form-control form-field', 'placeholder': 'Количество'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].input_formats = ['%Y-%m-%d']
