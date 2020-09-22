from django.shortcuts import render
from rest_framework.response import Response 
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.views import APIView 
from store.models import Product
from store.models import Customer
from store.models import Orderedproducts
from store.models import Order
from store.serializers import ProductAddSerializer,CustomerCreateSerializer,OrderCreateSeriliazer,GetOrderSerializerDateRange
from rest_framework.decorators import api_view
from rest_framework import status 
from rest_framework import request
import json,ast
import os
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import re
import csv
import pandas as pd
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from datetime import datetime

from django.db.models import Max
from django.db.models import Min

from django.db.models import Count


 #Adding the products
class ProductAddSet(APIView):
    def get(self, request, format=None):
        serializer = ProductAddSerializer()
        context_data = {"success" : False, "data" : serializer.data}    
        return Response(context_data)
    
    @method_decorator(csrf_exempt)
    def post(self, request,  format=None):
        serializer = ProductAddSerializer(data=request.data)
        if serializer.is_valid():
            #Verify Product
            
            product_obj_count = Product.objects.filter(product_number=request.data['product_number'])
            if product_obj_count.count() > 0:
                context_data = {"success" : False, "data" :{"message" : "Product Number Already Exists"}}
                return Response(context_data)
            try:
                product_details = {
                "product_number":request.data.get('product_number'),
                "name": request.data.get('name'),
                "brand": request.data.get('brand'),
                "description": request.data.get('description'),
                "price": request.data.get('price'),
                }
                if 'product_number' in request.data:
                        product_number = request.data['product_number']
                        product_number_check = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
                        if(product_number_check.search(product_number) != None):
                            context_data = {"success" : False, "errors" :{"message" : "Product Number should not contain special characters"}}
                            return Response(context_data)  
                #queryset = Product.objects.filter(product_number__product_number=request.data['product_number'])
                #product_data = queryset.values('product_number','name','brand','description','price','featured','active','created','modified')
                product_data = Product.objects.create(**product_details)
                queryset = Product.objects.filter(product_number=product_number).values('name','brand','description','price')
                context_data = {"success" : True, "data" :{"product_data": queryset, "message" : "Product Added Successfully"}}
            except Exception as e:
                #traceback.print_exc()
                context_data = {"success" : False, "errors" : {"message":str(e)}}
        else:
            context_data = {"success" : False, "errors" : {"message":"Not created" }}
        return Response(context_data)




        #GET PRODUCT DETAILS BY PRODUCT NUMBER
class ProductGet(APIView):
    def get(self,request, product_number=None, format=None):
        try:
            product_obj = Product.objects.get(product_number=product_number)
            product_data = []
            
            prod_get_objects ={
            "id":product_obj.id,
            "product_number":product_obj.product_number,
            "name":product_obj.name,
            "brand":product_obj.brand,
            "price":product_obj.price,
            "description":product_obj.description,
            "created":product_obj.created,
            "modified":product_obj.modified
            }
            product_data.append(prod_get_objects)
            context_data = {"success" : True, "data" :{"product_data" :prod_get_objects}}
        except Product.DoesNotExist as e:            
            context_data = {"success" : False, "errors" : {"message":"Product Record Does Not Exist"}}
            pass
        return Response(context_data)



 #delete the product by id
class DeleteOrder(APIView):
    def post(self,request,username=None):
        try:            
            prod_obj = Product.objects.get(pk=request.data['id'])
            prod_obj.delete()
            context_data = {"success" : True,"data" : {"message":'Order has been Deleted Successfully'}}
        except Product.DoesNotExist as e:
            context_data = {"success" : False,"errors" : {"message":"Order Does Not Exist"}}
        return Response(context_data) 



class CustomerCreate(APIView):
    def get(self, request, format=None):
        serializer = CustomerCreateSerializer()
        context_data = {"success" : False, "data" : serializer.data}    
        return Response(context_data)
    
    @method_decorator(csrf_exempt)
    def post(self, request,  format=None):
        serializer = CustomerCreateSerializer(data=request.data)
        if serializer.is_valid():
            #Verify Product
            
            customer_obj_count = Customer.objects.filter(customer_number=request.data['customer_number'],mobile_number=request.data['mobile_number'])
            if customer_obj_count.count() > 0:
                context_data = {"success" : False, "data" :{"message" : "Customer Already Exist"}}
                return Response(context_data)
        
            try:
                customer_details = {
                "customer_number":request.data.get('customer_number'),
                "first_name": request.data.get('first_name'),
                "last_name": request.data.get('last_name'),
                "email_id": request.data.get('email_id'),
                "mobile_number": request.data.get('mobile_number'),
                "address":request.data.get('address'),
                }


                if 'customer_number' in request.data:

                        
                        customer_number = request.data['customer_number']
                        customer_number_check = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
                        if(customer_number_check.search(customer_number) != None):
                            context_data = {"success" : False, "errors" :{"message" : "Customer Number should be Numerics"}}
                            return Response(context_data)  
                
                
                queryset = Customer.objects.filter(customer_number=customer_number).values('id','customer_number','first_name','last_name','email_id','mobile_number','address')
                #product_data = queryset.values('product_number','name','brand','description','price','featured','active','created','modified')
                customer_data = Customer.objects.create(**customer_details)
                context_data = {"success" : True, "data" :{"customer_data": queryset, "message" : "Customer created Successfully"}}
            except Exception as e:
                #traceback.print_exc()
                context_data = {"success" : False, "errors" : {"message":str(e)}}
        else:
            context_data = {"success" : False, "errors" : {"message":"Not created" }}
        return Response(context_data)


class DeleteCustomer(APIView):
    def post(self,request,pk=None):
        try:            
            cust_obj = Customer.objects.get(pk=request.data['id'])
            cust_obj.delete()
            context_data = {"success" : True,"data" : {"message":'Customer has Removed Successfully'}}
        except Customer.DoesNotExist as e:
            context_data = {"success" : False,"errors" : {"message":"No Customer is available with this Id"}}
        return Response(context_data) 


class GetCustomerDetails(APIView):
    def get(self,request, customer_number=None, format=None):
        try:
            cudtomer_obj = Customer.objects.get(customer_number=customer_number)
            customer_data = []
            
            cust_get_objects ={
            "id":cudtomer_obj.id,
            "first_name":cudtomer_obj.first_name,
            "last_name":cudtomer_obj.last_name,
            "email_id":cudtomer_obj.email_id,
            "mobile_number":cudtomer_obj.mobile_number,
            "address":cudtomer_obj.address,
            }

            customer_data.append(cust_get_objects)
            context_data = {"success" : True, "data" :{"product_data" :cust_get_objects}}
        except Customer.DoesNotExist as e:            
            context_data = {"success" : False, "errors" : {"message":"Customer Record Does Not Exist"}}
            pass
        return Response(context_data)



class OrderCreate(APIView):
    def get(self, request, format=None):
        serializer = OrderCreateSeriliazer()
        context_data = {"success" : False, "data" : serializer.data}    
        return Response(context_data)
    
    @method_decorator(csrf_exempt)
    def post(self, request,format=None):
        serializer = OrderCreateSeriliazer(data=request.data['id'])
        if serializer.is_valid():
            #Verify Product
            
            order_obj_count = Order.objects.filter(id=request.data['id'])
            if order_obj_count.count() > 0:
                context_data = {"success" : False, "data" :{"message" : "Order_Id Already Exist"}}
                return Response(context_data)
        
            try:
                order_details = {
                "total_amount":request.data.get('total_amount'),
                "order_date": request.data.get('order_date'),
                #"order_status": request.data.get('order_status'),
                "customer_id" : request.data.get('customer_id'),
                "billing_address": request.data.get('billing_address'),
                "shipping_address": request.data.get('shipping_address'),
                }
                #queryset = Product.objects.filter(product_number__product_number=request.data['product_number'])
                #product_data = queryset.values('product_number','name','brand','description','price','featured','active','created','modified')
                order_data = Order.objects.create(**order_details)
                context_data = {"success" : True, "data" :{"customer_data": order_data, "message" : "Your Order has Placed Successfully"}}
            except Exception as e:
                #traceback.print_exc()
                context_data = {"success" : False, "errors" : {"message":str(e)}}
        else:
            context_data = {"success" : False, "errors" : {"message":"Not created" }}
        return Response(context_data)



class GetOrderedDetails(APIView):
    def get(self,request,query_type):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        print(start_date,end_date)
        if query_type == 'json':
            try:

                ordered_obj_list = Order.objects.filter(order_date__range=[start_date,end_date])
                #ordered_obj_list = Order.objects.get(id=2)
                ordered_data = []
                for each_order_obj in ordered_obj_list:
                    ordered_get_objects ={
                    "order_id":each_order_obj.id,
                    "total_amount":each_order_obj.total_amount,
                    "customer":each_order_obj.id,
                    "first_name":each_order_obj.customer.first_name,
                    "last_name":each_order_obj.customer.last_name,
                    "mobile_number":each_order_obj.customer.mobile_number,
                    "email_id":each_order_obj.customer.email_id,
                    "address":each_order_obj.customer.address,
                    #"product":each_order_obj.id,
                    "shipping_address":each_order_obj.shipping_address,
                    "billing_address":each_order_obj.billing_address,
                    "order_date":each_order_obj.order_date,
                    }
                    ordered_data.append(ordered_get_objects)
                print ordered_data

                context_data = {"success" : True, "data" :{"ordered details" :ordered_data}}
            except Order.DoesNotExist as e:            
                context_data = {"success" : False, "errors" : {"message":"Record Does Not Exist"}}
                pass
            return Response(context_data)

            #CSV
        elif query_type =='csv':

            order_list =[]
            ordered_obj_list = Order.objects.filter(order_date__range=[start_date,end_date])

            for each_ord in ordered_obj_list:
                # first_name = each_ord.customer.first_name
                # last_name = each_ord.customer.last_name
                # mobile_number = each_ord.customer.mobile_number
                # email_id = each_ord.customer.mobile_number
                # address = each_ord.customer.address
                # shipping_address = each_ord.shipping_address
                # billing_address = each_ord.billing_address
                # order_date = each_ord.order_date
                total_amount = each_ord.total_amount

                order_list.append([first_name,last_name,mobile_number,email_id,address,shipping_address,billing_address,order_date,total_amount])

            response = HttpResponse(content_type='text/csv')
            current_date = datetime.now().strftime("%Y-%m-%d : %H-%M-%S %p")
            filename = "Order-Data-Download_{}.csv"
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
            field_names = ['first_name','last_name','mobile_number','email_id','address','shipping_address','billing_address','order_date','total_amount']

            writer=csv.writer(response)
            writer.writerow(field_names)
            writer.writerows(order_list)
            return response
        else:
            context_data = {"success":False,"errors":{"message": "query_type is not valid "}}
        return Response(context_data)




class AggregateView(APIView):
    def get(self,request,query_type):
        if query_type == 'Min':
            try:
                order_obj = Order.objects.aggregate(Min('total_amount'))
                context_data = {"success":True, "data":{"data":order_obj, "message": "Minimum price from the Order"}}
                return Response(context_data)
            except Exception as e:
                pass
        elif query_type == 'Max':
            try:
                order_obj = Order.objects.aggregate(Max('total_amount'))
                context_data = {"success":True, "data":{"data":order_obj, "message": "Maximum price from the Order"}}
                return Response(context_data)
            except Exception as e:
                pass
        else:
            context_data = {"success":False, "errors":{"message": "Give a valid query_type"}}
            return Response(context_data)



class SummaryReportView(APIView):
    def post(self,request,format=None):
        try:
            order_objects = Order.objects.filter(order_date=request.data['order_date']).count()
            context_data = {"success":True, "data" :order_objects, "message": "Number of orders are :"}
            return Response(context_data)
        except Order.DoesNotExist as e:
            context_data = {"success":False, "errors":{"message": "No record Found"}}
            pass






















# # def getcsv(request):
# #     response = HttpResponse(content_type='text/csv')  
# #     response['Content-Disposition'] = 'attachment; filename="order.csv"'  
# #     orders = Order.objects.all()  
# #     #orders = Order.objects.get(pk=order_id)
# #     writer = csv.writer(response)  
# #     for order in orders:  
# #         writer.writerow([order.id,order.total_amount, order.billing_address, order.shipping_address,order.order_date])
# #     return response  


# def getcsv(request):

#     # ordered_obj = []
#     ordered_obj=Order.objects.get(pk=order_id)
#     ordered_data = {
#             "order":request.GET.get('order'),
#             "total_amount":request.GET.get('total_amount'),
#             "customer":request.GET.get('customer'),
#             "first_name":request.GET.get('first_name'),
#             "last_name":request.GET.get('last_name'),
#             "mobile_number":request.GET.get('mobile_number'),
#             "email_id":request.GET.get('mobile_number'),
#             "address":request.GET.get('address'),
#             "shipping_address":request.GET.get('shipping_address'),
#             "billing_address":request.GET.get('billing_address'),
#             "order_date":request.GET.get('order_date'),
#             }

#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="order.csv"'  
#     columns = ['total_amount','first_name','last_name','mobile_number','email_id','address','shipping_address','billing_address','order_date'] 

#     writer = csv.writer(response)
#     writer.writerow(fields)

#     for Order in  ordered_obj:
#         # value = each_dict.ordered_data()
#         writer.writerow(fields)

#     return response



# class GetOrderedDetails(APIView):
#     def post(self,request):
#         serializer = GetOrderSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 ordered_data = []
#                 if request.data['query_type'] == 'json':
#                     try:
#                         ordered_obj = Order.objects.get(id=request.data['id'])
#                         ordered_get_objects ={
#                                 "order":ordered_obj.id,
#                                 "total_amount":ordered_obj.total_amount,
#                                 "customer":ordered_obj.id,
#                                 "first_name":ordered_obj.customer.first_name,
#                                 "last_name":ordered_obj.customer.last_name,
#                                 "mobile_number":ordered_obj.customer.mobile_number,
#                                 "email_id":ordered_obj.customer.email_id,
#                                 "address":ordered_obj.customer.address,
#                                 "product":ordered_obj.id,
#                                 #"name":product_obj.product.name,
#                                 "shipping_address":ordered_obj.shipping_address,
#                                 "billing_address":ordered_obj.billing_address,
#                                 "order_date":ordered_obj.order_date,
#                                 }
#                         ordered_data.append(ordered_get_objects)
#                         context_data = {"success" : True, "data" :{"ordered details" :ordered_get_objects}}
#                     except Order.DoesNotExist as e:            
#                             context_data = {"success" : False, "errors" : {"message":"Record Does Not Exist"}}
#             except Order.DoesNotExist as e:            
#                     context_data = {"success" : False, "errors" : {"message":"Record Does Not Exist"}}
#                     return Response(context_data)

#                 elif request.data['query_type'] == 'csv':
#                     try:
#                         ordered_obj = Order.objects.get(id=request.data['id'])
#                         try:

#                             response = HttpResponse(content_type='text/csv')
#                             filename = "Order-List_{}.csv"
#                             response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

#                             field_names = ['total_amount']

#                             writer=csv.writer(response)
#                             writer.writerow[ordered_obj.total_amount]

#                         except Order.DoesNotExist as e:
#                             context_data = {"success" : False, "errors" : {"message":"Record Does Not Exist"}}

#                         return response

#                 else:
#                     context_data = {"success":False,"errors":{"message": "query_type is not valid "}}
#                 return response(context_data)



