from django.test import TestCase
from .models import Category, Transaction

class CategoryModelTest(TestCase):
    def setUp(self):
        Category.objects.create(name='Test Category')
    
    def test_category_name(self):
        category = Category.objects.get(id=1)
        expected_object_name = f'{category.name}'
        self.assertEqual(expected_object_name, 'Test Category')

class TransactionModelTest(TestCase):
    def setUp(self):
        Transaction.objects.create(date='2021-09-01', description='Test Transaction', amount=100.00)
    
    def test_transaction_description(self):
        transaction = Transaction.objects.get(id=1)
        expected_object_name = f'{transaction.description}'
        self.assertEqual(expected_object_name, 'Test Transaction')
    
    def test_transaction_amount(self):
        transaction = Transaction.objects.get(id=1)
        expected_object_name = f'{transaction.amount}'
        self.assertEqual(expected_object_name, '100.00')