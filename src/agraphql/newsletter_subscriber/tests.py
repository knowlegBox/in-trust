import json
from django.test import TestCase
from graphene.test import Client
from ..schema import schema
from api import models

class NewsletterSubscriberTestCase(TestCase):
    def setUp(self):
        # Create test data here
        self.test_instance = models.NewsletterSubscriber.objects.create(
            # Add required fields here, e.g.:
            # field_name='value',
        )

    def test_query_newsletter_subscriber(self):
        # Test querying NewsletterSubscriber
        client = Client(schema)
        query = '''
        query {
            newsletter_subscriberList {
                edges {
                    node {
                        id
                    }
                }
            }
        }
        '''
        executed = client.execute(query)
        self.assertIsNotNone(executed.get('data'))
        self.assertIn('newsletter_subscriberList', executed.get('data'))

    def test_create_newsletter_subscriber(self):
        # Test creating NewsletterSubscriber
        client = Client(schema)
        mutation = '''
        mutation CreateNewsletterSubscriber {
            createNewsletterSubscriber(
                # Add required fields here, e.g.:
                # field_name: "value"
            ) {
                success
                message
                newsletter_subscriber {
                    id
                }
                errors
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['createNewsletterSubscriber']['success'])
        self.assertIsNotNone(executed['data']['createNewsletterSubscriber'][NewsletterSubscriber.lower()]['id'])

    def test_update_newsletter_subscriber(self):
        # Test updating NewsletterSubscriber
        client = Client(schema)
        mutation = '''
        mutation UpdateNewsletterSubscriber {
            updateNewsletterSubscriber(
                id: self.test_instance.id,
                # Add fields to update here, e.g.:
                # field_name: "new_value"
            ) {
                success
                message
                newsletter_subscriber {
                    id
                }
                errors
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['updateNewsletterSubscriber']['success'])

    def test_delete_newsletter_subscriber(self):
        # Test deleting NewsletterSubscriber
        client = Client(schema)
        mutation = '''
        mutation DeleteNewsletterSubscriber {
            deleteNewsletterSubscriber(
                id: self.test_instance.id
            ) {
                success
                message
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['deleteNewsletterSubscriber']['success'])
