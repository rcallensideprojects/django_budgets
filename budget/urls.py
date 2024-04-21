from django.urls import path
from . import views

# app_name = 'budget'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('create_category/', views.create_category, name='create_category'),
    path('update_transaction/<int:transaction_id>/', views.update_transaction, name='update_transaction'),
    path('transactions_filtered/<str:month>/<str:category>/', views.transactions_filtered, name='transactions_filtered'),
    path('category_index/', views.category_index, name='category_index'),
    path('update_category/<int:category_id>/', views.update_category, name='update_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    # Other URL patterns...
]
