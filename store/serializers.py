from rest_framework import serializers

from models import * 
from store.models import Product

class ProductAddSerializer(serializers.Serializer):
    product_number = models.CharField(max_length=100,unique=True)
    name = models.CharField(max_length=250)
    brand = models.CharField(max_length=250, blank=True)
    description = models.CharField(max_length=300,blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    # active = models.BooleanField(default=True)
    # created = models.DateTimeField(auto_now_add=True)
    # modified = models.DateTimeField(auto_now=True)


    def validate_product_number(self,value):
        value=value.replace(' ',' ')
        if not value.isnumeric():
            raise serializers.ValidationError("Product Number should be a digit")

class CustomerCreateSerializer(serializers.Serializer):
    customer_number = models.CharField(max_length=100,unique=True)
    first_name = models.CharField(max_length=250,null=True,blank=True)
    last_name = models.CharField(max_length=250,null=True,blank=True)
    email_id = models.CharField(max_length=250,null=True,blank=True)
    mobile_number = models.CharField(max_length=250,null=True,blank=True)
    address = models.CharField(max_length=250,null=True,blank=True)

    def validate_first_name(self,value):
    	value = value.replace(' ','')
    	if len(value) > 20:
    		raise serializers.ValidationError("First Name Should Not be More than 30 Characters")
    	if not value.isalpha():
    		raise serializers.ValidationError("First Name Should Contains Character Only")	
    
    def validate_last_name(self, value):
        value = value.replace(' ','')
        if len(value) > 20:
            raise serializers.ValidationError("Name Should Not Be More Than 30 Characters")
        if not value.isalpha():
            raise serializers.ValidationError("Surname Should Contains Character Only")

	def validate_mobile_number(self, value):
	    value = value.replace(' ', '')
	    if len(value) != 10:
	        raise serializers.ValidationError("Mobile Number Length Must Be 10 Digits")
	    if not value.isnumeric():
	        raise serializers.ValidationError("Mobile Number Must Be Digits")
	    if not str(value).startswith(('6','7','8','9')):
	        raise serializers.ValidationError("Invalid mobile number")
	    return value

    def validate_email_id(self):
        email = self.cleaned_data["email"]
        if " " in email:
            raise forms.ValidationError('Enter a vaild email')
        elif email:
            email = email.replace(' ','')
            if not re.match("^(?!\.)[a-zA-Z0-9_,]*\.?[\.?a-zA-Z0-9_]+@[a-zA-Z]+\.(([a-zA-Z]{3})|([a-zA-Z]{2}\.[a-zA-Z]{2}))$",email):
                raise forms.ValidationError('Enter a vaild email')
        return self.cleaned_data['email']



# class ProductGetSerializer(serializers.Serializer):
#     product_no = models.CharField(max_length=200)

class OrderCreateSeriliazer(serializers.Serializer):
    customer = models.ForeignKey(Customer)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    order_date = models.DateTimeField(auto_now_add=True,null=True)
    oder_status = models.BooleanField(default=True)
    billing_address = models.CharField(max_length=250)
    shipping_address = models.CharField(max_length=250)


class GetOrderSerializerDateRange(serializers.Serializer):
    #query_type = models.CharField(max_length=100)
    from_date = models.CharField(max_length=100)
    to_date = models.CharField(max_length=100)