
from django.urls import path
from store import views


urlpatterns = [
   path('',views.Home.as_view(),name="home"),
   path('register/',views.Registerview.as_view(),name="register"),
   path('login/',views.Loginview.as_view(),name="log"),
   path('logout/',views.logoutView.as_view(),name="logout"),
   path('Category/<int:pk>',views.Category_detail.as_view(),name='category'),
   path('product/<int:pk>',views.Product_detail.as_view(),name="product"),
   path('cart/<int:pk>',views.Cartview.as_view(),name="cart"),
   path('cartdelete/<int:pk>',views.Cartdelete.as_view(),name="cartdelete"),
   path('cartdetails/',views.Cartdetails.as_view(),name="cartdetails"),
   path('orderview/<int:pk>',views.Orderview.as_view(),name='order'),
   path('orderlist/',views.order_list.as_view(),name="order_list"),
   path('remove_order/<int:pk>',views.remove_order.as_view(),name="remove_order")
  
] 
