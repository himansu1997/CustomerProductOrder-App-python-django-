from django.conf.urls import include, url

from store import views


urlpatterns = [
    #url(r'^createproduct/$', views.ProductCreate.as_view(), name="createproduct"),
    url(r'^create/product$', views.ProductCreate.as_view(), name="create_product"),
    #url(r'^get_product/$', views.OrderCreate.as_view(), name="get_product"),
    url(r'^add_customer/$', views.CustomerCreate.as_view(), name="add_customer"),
    url(r'^customer/get/$', views.CustomerCreate.as_view(), name="add_customer"),
    url(r'^products/get$', views.ProductGet.as_view(), name="createproduct"),
    url(r'^order/add$', views.OrderCreate.as_view(), name="createproduct"),

    
]