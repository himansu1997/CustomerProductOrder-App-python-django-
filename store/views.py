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
from store.serializers import ProductAddSerializer,CustomerCreateSerializer,OrderCreateSeriliazer
from rest_framework.decorators import api_view

from rest_framework import status 
from rest_framework import request
import json,ast
import os

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import re

import csv

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
            
            customer_obj_count = Customer.objects.filter(customer_number=request.data['customer_number'])
            if customer_obj_count.count() > 0:
                context_data = {"success" : False, "data" :{"message" : "Customer Number Already Exist"}}
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

                        
                        product_number = request.data['customer_number']
                        product_number_check = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
                        if(product_number_check.search(product_number) != None):
                            context_data = {"success" : False, "errors" :{"message" : "Customer Number should be Numerics"}}
                            return Response(context_data)  
                
                
                #queryset = Product.objects.filter(product_number__product_number=request.data['product_number'])
                #product_data = queryset.values('product_number','name','brand','description','price','featured','active','created','modified')
                customer_data = Customer.objects.create(**customer_details)
                context_data = {"success" : True, "data" :{"customer_data": customer_data, "message" : "Product Added Successfully"}}
            except Exception as e:
                #traceback.print_exc()
                context_data = {"success" : False, "errors" : {"message":str(e)}}
        else:
            context_data = {"success" : False, "errors" : {"message":"Not created" }}
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
    def post(self, request,  format=None):
        serializer = OrderCreateSeriliazer(data=request.data)
        if serializer.is_valid():
            #Verify Product
            
            order_obj_count = Order.objects.filter(id=pk)
            if order_obj_count.count() > 0:
                context_data = {"success" : False, "data" :{"message" : "Order Number Already Exist"}}
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


                # if 'customer_number' in request.data:

                        
                #         product_number = request.data['customer_number']
                #         product_number_check = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
                #         if(product_number_check.search(product_number) != None):
                #             context_data = {"success" : False, "errors" :{"message" : "Customer Number should be Numerics"}}
                #             return Response(context_data)  
                
                
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
    def get(self,request, order_id=None, format=None):
        try:
            #ordered_obj = Orderedproducts.objects.get(product_number=product_number)
            ordered_obj = Order.objects.get(pk=order_id)

            #customer_obj=
            #ordered_obj = Customer.objects.filter().values(customer_number=request.data['customer_number']).values('first_name')
            ordered_data = []
            
            ordered_get_objects ={
            "order":ordered_obj.id,
            "total_amount":ordered_obj.total_amount,
            "customer":ordered_obj.id,
            "product":ordered_obj.id,
            "shipping_address":ordered_obj.shipping_address,
            "billing_address":ordered_obj.billing_address,
            "order_date":ordered_obj.order_date,







            }
            ordered_data.append(ordered_get_objects)
            context_data = {"success" : True, "data" :{"ordered details" :ordered_get_objects}}
        except Order.DoesNotExist as e:            
            context_data = {"success" : False, "errors" : {"message":"Record Does Not Exist"}}
            pass
        return Response(context_data)

