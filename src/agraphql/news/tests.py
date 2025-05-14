import json
from django.test import TestCase
from graphene.test import Client
from ..schema import schema
from api import models

class NewsTestCase(TestCase):
    def setUp(self):
        # Create test data here
        self.test_instance = models.News.objects.create(
            # Add required fields here, e.g.:
            # field_name='value',
        )

    def test_query_news(self):
        # Test querying News
        client = Client(schema)
        query = '''
        query {
            newsList {
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
        self.assertIn('newsList', executed.get('data'))

    def test_create_news(self):
        # Test creating News
        client = Client(schema)
        mutation = '''
        mutation CreateNews {
            createNews(
                # Add required fields here, e.g.:
                # field_name: "value"
            ) {
                success
                message
                news {
                    id
                }
                errors
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['createNews']['success'])
        self.assertIsNotNone(executed['data']['createNews'][News.lower()]['id'])

    def test_update_news(self):
        # Test updating News
        client = Client(schema)
        mutation = '''
        mutation UpdateNews {
            updateNews(
                id: self.test_instance.id,
                # Add fields to update here, e.g.:
                # field_name: "new_value"
            ) {
                success
                message
                news {
                    id
                }
                errors
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['updateNews']['success'])

    def test_delete_news(self):
        # Test deleting News
        client = Client(schema)
        mutation = '''
        mutation DeleteNews {
            deleteNews(
                id: self.test_instance.id
            ) {
                success
                message
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['deleteNews']['success'])
