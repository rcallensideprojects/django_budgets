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
        csv_file = SimpleUploadedFile("test.csv", b"Posting Date,Description,Amount\n2024-04-19,Test Purchase,10.00", content_type="text/csv")
        response = self.client.post(reverse('budget:upload_csv'), {'file': csv_file}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        expected_date = datetime.strptime('2024-04-19', '%Y-%m-%d').date()
        self.assertEqual(transaction.date, expected_date)
    
    def test_upload_invalid_csv(self):
        invalid_csv_file = SimpleUploadedFile("invalid.csv", b"Posting Date,Description,Amount\n2024-04-19,10.00", content_type="text/csv")
        response = self.client.post(reverse('budget:upload_csv'), {'file': invalid_csv_file}, follow=True)
