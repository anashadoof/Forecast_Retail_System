from django.urls import path
from . import views

urlpatterns = [
    path('', views.database_home, name='database_home'),
    path('add_store', views.add_store, name='add_store'),
    path('delete_store/(?P<store_id>[0-9]+)/$', views.delete_store, name='delete_store'),
    path('delete_product/(?P<product_id>[0-9]+)/$', views.delete_product, name='delete_product'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_promo/', views.add_promo, name='add_promo'),
    path('add_sales/', views.add_sale, name='add_sale'),
    path('delete_promo/(?P<promo_id>[0-9]+)/$', views.delete_promo, name='delete_promo'),
    path('delete_sale/<int:sale_id>/', views.delete_sale, name='delete_sale'),
    path('edit_store/(?P<store_id>[0-9]+)/$', views.edit_store, name='edit_store'),
    path('edit_product/(?P<product_id>[0-9]+)/$', views.edit_product, name='edit_product'),
    path('edit_promo/(?P<promo_id>[0-9]+)/$', views.edit_promo, name='edit_promo'),
    path('edit_sale/<int:sale_id>/', views.edit_sale, name='edit_sale'),
]
