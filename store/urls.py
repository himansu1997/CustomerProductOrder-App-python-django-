from django.conf.urls import include, url

from store import views


urlpatterns = [
    #url(r'^createproduct/$', views.ProductCreate.as_view(), name="createproduct"),

    #PRODUCT URL
    url(r'^add/product$', views.ProductAddSet.as_view(), name="add_product"),
    url(r'^products/(?P<product_number>[\w-]+)/get$', views.ProductGet.as_view(), name='product_view_api'),

    #url(r'^get_product/$', views.OrderCreate.as_view(), name="get_product"),

    #CUSTOMER URL'S
    url(r'^add_customer/$', views.CustomerCreate.as_view(), name="add_customer"),
    url(r'^customer/(?P<customer_number>[\w-]+)/get$', views.GetCustomerDetails.as_view(), name="get_customer_api"),


    url(r'^products/get$', views.ProductGet.as_view(), name="get_product"),
    url(r'^order/add$', views.OrderCreate.as_view(), name="create_order"),

    #url(r'^orderd_details/(?P<order_id>[\w-]+)/get$', views.GetOrderedDetails.as_view(), name="get_all_data"),

    #url(r'^orderd_csv/get$', views.getcsv, name="get_all_data_csv"),

    #url(r'^orderdcsvreport/get$', views.OrderCsvReportViewSet, name="get_all_data_csv"),


    url(r'^orderd_details/get$', views.GetOrderedDetails.as_view(), name="get_all_data"),

    url(r'^orderd_details/(?P<order_id>[\w-]+)/(?P<query_type>\w+)$',views.GetOrderedDetails.as_view()),
]