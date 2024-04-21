from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from budget.models import Transaction, Category
from datetime import datetime

class UploadCSVViewTests(TestCase):
    def test_upload_page_render(self):
        # Test that the upload page renders successfully
        response = self.client.get(reverse('budget:upload_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/upload_csv.html')
    
    def test_upload_valid_csv(self):
        csv_file = SimpleUploadedFile("test.csv", b"Posting Date,Description,Amount\n04/19/2024,Test Purchase,10.00", content_type="text/csv")
        response = self.client.post(reverse('budget:upload_csv'), {'csv_file': csv_file}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        expected_date = datetime.strptime('04/19/2024', '%m/%d/%Y').date()
        self.assertEqual(transaction.date, expected_date)

    def test_upload_duplicate_transactions(self):
        csv_file = SimpleUploadedFile("test.csv", b"Posting Date,Description,Amount\n04/19/2024,Test Purchase,10.00", content_type="text/csv")
        response = self.client.post(reverse('budget:upload_csv'), {'csv_file': csv_file}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Transaction.objects.count(), 1)
        response = self.client.post(reverse('budget:upload_csv'), {'csv_file': csv_file}, follow=True)
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        expected_date = datetime.strptime('04/19/2024', '%m/%d/%Y').date()
        self.assertEqual(transaction.date, expected_date)
    
        
class CreateCategoryViewTests(TestCase):
    def test_create_category(self):
        # Test that a category can be created
        response = self.client.post(reverse('budget:create_category'), {'name': 'Test Category', 'order': 0}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.count(), 1)
        category = Category.objects.first()
        self.assertEqual(category.name, 'Test Category')
    
    def test_create_category_redirect(self):
        # Test that the user is redirected to the transactions page after creating a category
        response = self.client.post(reverse('budget:create_category'), {'name': 'Test Category'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/transactions.html')

class TransactionsViewTests(TestCase):
    def test_transactions_page_render(self):
        # Test that the transactions page renders successfully
        response = self.client.get(reverse('budget:transactions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/transactions.html')
    
    def test_transactions_list(self):
        # Test that the transactions list is displayed correctly
        Transaction.objects.create(date=datetime.strptime('04/19/2024', '%m/%d/%Y').date(), description='Test Purchase', amount=10.00)
        response = self.client.get(reverse('budget:transactions'))
        self.assertContains(response, 'Test Purchase')
        self.assertContains(response, '10.00')
        self.assertContains(response, 'April 19, 2024')

class IndexViewTests(TestCase):
    def test_index_page_render(self):
        # Test that the index page renders successfully
        response = self.client.get(reverse('budget:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/index.html')
    
    def test_index_kpis(self):
        # Test that the KPIs are displayed correctly
        Transaction.objects.create(date=datetime.strptime('04/19/2024', '%m/%d/%Y').date(), description='Test Purchase', amount=10.00)
        response = self.client.get(reverse('budget:index'))
        self.assertContains(response, 'April 2024')
        self.assertContains(response, 'None')
        self.assertContains(response, '10')

class CategoryIndexViewTests(TestCase):
    def test_category_index_page_render(self):
        # Test that the category index page renders successfully
        response = self.client.get(reverse('budget:category_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/category_index.html')
    
    def test_category_index_list(self):
        # Test that the category index list is displayed correctly
        Category.objects.create(name='Test Category')
        response = self.client.get(reverse('budget:category_index'))
        self.assertContains(response, 'Test Category')

