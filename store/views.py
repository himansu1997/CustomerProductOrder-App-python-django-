from django.shortcuts import render
from rest_framework.response import Response 
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.views import APIView 
from store.models import Product
from store.models import Customer
from store.models import Orderedproducts
from store.serializers import ProductAddSerializer,CustomerCreateSerializer,OrderCreateSerializer
from rest_framework.decorators import api_view

from rest_framework import status 
from rest_framework import request
import json,ast
import os

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import re


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
                context_data = {"success" : True, "data" :{"product_data": product_data, "message" : "Product Added Successfully"}}
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
            "active":product_obj.active,
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


                # if 'product_number' in request.data:

                        
                #         product_number = request.data['product_number']
                #         product_number_check = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
                #         if(product_number_check.search(product_number) != None):
                #             context_data = {"success" : False, "errors" :{"message" : "Product Number should not contain special characters"}}
                #             return Response(context_data)  
                
                
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



class GrtOredrDetails(APIView):
    def post(self,request,format=None):
        serializer = CustomerGetSerializer(data=request.data)
        if serializer.is_valid():
            order_id = request.data['id']
            
            try:
                    order_obj = Customer.objects.filter(id=id).values
                    #product_data.append(products_obj)
                    context_data = {"success" : True, "data" : products_obj}
            except Customer.DoesNotExist:
                    context_data = {"success" : False, "errors" : {"message": "Id Does Not Exist" }}
                    pass
        else:
            print serializer.errors
            context_data = {"success" : False, "errors" : {"message": "Validation Error" ,  "errors_list" :serializer.errors}}
        return Response(context_data)



class OrderCreate(APIView):
    def post(serializers,request,format=None):
        serializer= OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




