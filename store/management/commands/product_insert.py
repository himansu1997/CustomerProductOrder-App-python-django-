import os
import random
from django.core.management.base import BaseCommand
from store.models import *
import decimal


def random_string_generator(size, type=None):
	if type == "char":
		chars = chars = string.ascii_uppercase + string.ascii_lowercase
	return ''.join(random.choice(chars) for _ in range(size))

class Command(BaseCommand):
	help = 'Insert random products'

	def add_arguments(self,parser):
		parser.add_argument('total', type=int, help='Indicates the number of products to be created')

	def handle(self, *args, **kwargs):
		total = kwargs['total']


		category_choices = ['Laptop','Mobile','Electronic Accessories','Fashion','Sports & Fitness','Books']
		brand_choices = ['Hp','Dell','Nike','Asus','LG']

		for i in range(total):
			Product.objects.create(product_number=random.randint(1,500),
				name= random_string_generator(10,'char'),
				brand=random.choice(brand_choices),
				description=random_string_generator(50,'char'),
				sale_price=decimal.Decimal(random.randrange(4567,67890)),
				product_category =ranom.choice(category_choices)
				 )
			#Product.objects.create(product_number=random.randint(1,10),name=get_random_string(),brand=get_random_string(),description=get_random_string(),price='', )

		
