import os
import random
from django.core.management.base import BaseCommand
from store.models import *
import decimal
import string


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

		for i in range(total):
			Order.objects.create(
				total_amount=decimal.Decimal(random.randrange(4567,67890)),
				billing_address=random_string_generator(10,'char'),
				shipping_address=random_string_generator(50,'char'),
				 )