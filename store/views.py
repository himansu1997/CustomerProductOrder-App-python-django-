from django.shortcuts import render
from rest_framework.response import Response 
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.views import APIView 
from store.models import Product
from store.serializers import ProductCreateSerializer,ProductGetSerializer,CustomerCreateSerializer,OrderCreateSerializer
from rest_framework.decorators import api_view

from rest_framework import status 
from rest_framework import request
import json,ast
import os

class ProductCreate(APIView):
    def post(self,request,format=None):
        serializer = ProductCreateSerializer(data=request.data)
        #try:
        if serializer.is_valid():
            serializer.save()
            print("executed")
        #except Exception as e:
            return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)   


class ProductGet(APIView):
    def post(self, request,format=None):
        serializer = ProductGetSerializer(data=request.data)
        if serializer.is_valid():
            product_number = request.data['product_number']
            
            try:
                    products_obj = Product.objects.filter(product_number=request.data['product_number']).values('name','brand','shipping','price','description','featured','active','created','modified')
                    #product_data.append(products_obj)
                    context_data = {"success" : True, "data" : products_obj}
            except Product.DoesNotExist:
                    context_data = {"success" : False, "errors" : {"message": "Invalid product_no" }}
                    pass
        else:
            print serializer.errors
            context_data = {"success" : False, "errors" : {"message": "Validation Error" ,  "errors_list" :serializer.errors}}
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


class OrderCreate(APIView):
    def post(serializers,request,format=None):
        serializer= OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CustomerCreate(APIView):
    def post(self,request,format=None):
        serializer = CustomerCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class GetCustomerDetails(APIView):
    def post(self, request,format=None):
        serializer = CustomerGetSerializer(data=request.data)
        if serializer.is_valid():
            cust_id = request.data['id']
            
            try:
                    customer_obj = Customer.objects.filter(id=id).values('name','brand','shipping','price','description','featured','active','created','modified')
                    #product_data.append(products_obj)
                    context_data = {"success" : True, "data" : customer_obj}
            except Customer.DoesNotExist:
                    context_data = {"success" : False, "errors" : {"message": "Id Does Not Exist" }}
                    pass
        else:
            print serializer.errors
            context_data = {"success" : False, "errors" : {"message": "Validation Error" ,  "errors_list" :serializer.errors}}
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