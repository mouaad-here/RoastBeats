import json
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from unittest.mock import patch

@override_settings(DEBUG=True)
class PageLoadTests(TestCase):
    """
    Sanity Checks: Do the URLs actually work?
    """
    def setUp(self):
        self.client = Client()

    def test_homepage_loads(self):
        """Test if the index page loads with status 200"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_manual_input_page_loads(self):
        """Test if the manual input page loads"""
        response = self.client.get(reverse('roast_manual'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manual_input.html')

    def test_404_page(self):
        """Test that a made-up URL returns a 404 error"""
        response = self.client.get('/this-url-does-not-exist/')
        self.assertEqual(response.status_code, 404)

@override_settings(DEBUG=True)
class ManualFlowTests(TestCase):
    """
    Test the Manual Input Logic (Session handling & Redirects)
    """
    def setUp(self):
        self.client = Client()

    def test_manual_form_submission(self):
        """
        When a user submits the manual form, it should:
        1. Save data to session.
        2. Redirect to the loading page ('roast_me').
        """
        form_data = {
            'username': 'Test User',
            'music_taste': 'I love Nickelback and silence.'
        }
        
        # Simulate POST request
        response = self.client.post(reverse('roast_manual'), form_data)
        
        # Check for Redirect (302)
        self.assertRedirects(response, reverse('roast_me'))
        
        # Check if data was saved to session
        session = self.client.session
        self.assertEqual(session['roast_source'], 'manual')
        self.assertEqual(session['manual_data']['username'], 'Test User')

@override_settings(DEBUG=True)
class ApiTests(TestCase):
    """
    Test the JSON API endpoint.
    We use @patch to MOCK the AI call so we don't spend API credits.
    """
    def setUp(self):
        self.client = Client()

    # We intercept 'core.views.get_ai_roast' and replace it with 'mock_get_roast'
    @patch('core.views.get_ai_roast')
    def test_roast_api_manual(self, mock_get_roast):
        """
        Test that the API reads from session and returns JSON.
        """
        # 1. Setup the Fake AI Response (The Mock)
        mock_get_roast.return_value = {
            "headline": "Mocked Headline",
            "score": 100,
            "roast_body": "This is a fake roast for testing.",
            "dating_life": "Forever alone"
        }

        # 2. Setup the User Session (Simulate a user who just filled the form)
        session = self.client.session
        session['roast_source'] = 'manual'
        session['manual_data'] = {
            'username': 'Tester', 
            'music_input': 'Test Music'
        }
        session.save() # Must save to apply changes

        # 3. Call the API Endpoint
        response = self.client.get(reverse('roast_api_data'))

        # 4. Assertions (The Proof)
        self.assertEqual(response.status_code, 200)
        
        # Convert response to JSON
        data = response.json()
        
        # Did we get our fake data back?
        self.assertEqual(data['headline'], "Mocked Headline")
        self.assertEqual(data['score'], 100)
