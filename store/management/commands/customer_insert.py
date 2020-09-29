import random
from store.models import Customer
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


# def Email():
	# 	mail_extensions = ['com','net','org']
	# 	mail_domains = ['gmail','yahoo','outlook']

	# 	mail_ext = mail_extensions[random.randint(0,len(mail_extensions)-1)]
	# 	mail_dom = mail_domains[random.randint[0,len(mail_domains)-1]]


class Command(BaseCommand):
	help = 'insert customer data'

	def add_arguments(self,parser):
		parser.add_argument('total', type=int, help='the number of customer to be created')

	def handle(self, *args, **kwargs):
		total = kwargs['total']

		#address_choices = ['Hyderabad','Pune','Bangalore','Kolkata','Mumbai','Odisha']
		for i in range(total):
			Customer.objects.create(
				customer_number=random.randint(1,500),
				first_name= random_string_generator(15,'char'),
				last_name=random_string_generator(15,'char'),
				email_id=random_email(5)+"@gmail.com",
				mobile_number =random_mobile_generator(), 
				address= random_string_generator(15,'char'), 
				)


	
