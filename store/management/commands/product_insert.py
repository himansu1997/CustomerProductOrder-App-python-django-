import os
import random
from django.core.management.base import BaseCommand
from store.models import *
import decimal


class Command(BaseCommand):
	help = 'Insert random products'

	def add_arguments(self,parser):
		parser.add_argument('total', type=int, help='Indicates the number of products to be created')

	def handle(self, *args, **kwargs):
		total = kwargs['total']
		name_choices = ['Laptop','Shoe','Mobile']
		brand_choices = ['Hp','Dell','Nike','Asus']
		description_choices = ['4gb ram with 512gb ssd','blue in clolour','nice features']
		for i in range(total):
			Product.objects.create(product_number=random.randint(1,500),name= random.choice(name_choices),brand=random.choice(brand_choices),description=random.choice(description_choices),price=decimal.Decimal(random.randrange(4567,67890)) )
			#Product.objects.create(product_number=random.randint(1,10),name=get_random_string(),brand=get_random_string(),description=get_random_string(),price='', )

		
