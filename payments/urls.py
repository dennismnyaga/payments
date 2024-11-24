from django.urls import path
from . import views

urlpatterns = [
    # path('', views.PaymentService.as_view())
    path('', views.index),
    path('purchase/<uuid:repository_id>/', views.purchase_repository, name='purchase_repository'),
    path('save-email/', views.save_buyer_email, name='save_buyer_email'),
]