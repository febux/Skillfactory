from django.urls import path
from .views import ProductsList, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView
# импортируем наше представление

urlpatterns = [
    path('', ProductsList.as_view()),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),  # Ссылка на детали товара
    path('create/', ProductCreateView.as_view(), name='product_create'),  # Ссылка на создание товара
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),  # Ссылка на создание товара
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),  # Ссылка на создание товара
]
