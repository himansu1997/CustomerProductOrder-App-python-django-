import random
from store.models import Vendor
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
import string


def random_mobile_generator():
	first = str(random.randint(600, 999))
	second = str(random.randint(1, 888))
	last = (str(random.randint(1, 9998)).zfill(4))
	return '{}{}{}'.format(first, second, last)

def random_string_generator(size, type=None):
	if type == "char":
		chars = chars = string.ascii_uppercase + string.ascii_lowercase
	return ''.join(random.choice(chars) for _ in range(size))

def random_email(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))


class Command(BaseCommand):
	help = 'insert customer data'

	def add_arguments(self,parser):
		parser.add_argument('total', type=int, help='the number of vendors to be created')

	def handle(self, *args, **kwargs):
		total = kwargs['total']

		for i in range(total):
			Vendor.objects.create(
				vendor_store_name= random_string_generator(15,'char'),
				vendor_store_email=random_email(5)+"@gmail.com",
				vendor_store_number =random_mobile_generator(), 
				vendor_store_address= random_string_generator(15,'char'), 
				)


	
