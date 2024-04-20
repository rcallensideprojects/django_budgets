from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from budget.models import Transaction
from datetime import datetime

class UploadCSVViewTests(TestCase):
    def test_upload_page_render(self):
        # Test that the upload page renders successfully
        response = self.client.get(reverse('budget:upload_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/upload_csv.html')
    
    def test_upload_valid_csv(self):
        # Test that a POST request with a valid CSV file uploads successfully
        # Create a sample CSV file
        csv_file = SimpleUploadedFile("test.csv", b"Posting Date,Description,Amount\n2024-04-19,Test Purchase,10.00", content_type="text/csv")
        # Submit a POST request with the CSV file
        response = self.client.post(reverse('budget:upload_csv'), {'file': csv_file}, follow=True)
        # Add assertions to check that the file is uploaded successfully and the data is saved to the database
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        expected_date = datetime.strptime('2024-04-19', '%Y-%m-%d').date()
        self.assertEqual(transaction.date, expected_date)
    
    def test_upload_invalid_csv(self):
        # Test that a POST request with an invalid CSV file displays appropriate error messages
        # Create a sample invalid CSV file (e.g., missing required columns)
        invalid_csv_file = SimpleUploadedFile("invalid.csv", b"Posting Date,Description,Amount\n2024-04-19,10.00", content_type="text/csv")
        # Submit a POST request with the invalid CSV file
        response = self.client.post(reverse('budget:upload_csv'), {'file': invalid_csv_file}, follow=True)
        # Add code to submit the POST request to the upload view
        # Add assertions to check that the appropriate error messages are displayed