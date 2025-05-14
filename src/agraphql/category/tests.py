import json
from django.test import TestCase
from graphene.test import Client
from ..schema import schema
from api import models

class CategoryTestCase(TestCase):
    def setUp(self):
        # Create test data here
        self.test_instance = models.Category.objects.create(
            # Add required fields here, e.g.:
            # field_name='value',
        )

    def test_query_category(self):
        # Test querying Category
        client = Client(schema)
        query = '''
        query {
            categoryList {
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
        self.assertIn('categoryList', executed.get('data'))

    def test_create_category(self):
        # Test creating Category
        client = Client(schema)
        mutation = '''
        mutation CreateCategory {
            createCategory(
                # Add required fields here, e.g.:
                # field_name: "value"
            ) {
                success
                message
                category {
                    id
                }
                errors
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['createCategory']['success'])
        self.assertIsNotNone(executed['data']['createCategory'][Category.lower()]['id'])

    def test_update_category(self):
        # Test updating Category
        client = Client(schema)
        mutation = '''
        mutation UpdateCategory {
            updateCategory(
                id: self.test_instance.id,
                # Add fields to update here, e.g.:
                # field_name: "new_value"
            ) {
                success
                message
                category {
                    id
                }
                errors
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['updateCategory']['success'])

    def test_delete_category(self):
        # Test deleting Category
        client = Client(schema)
        mutation = '''
        mutation DeleteCategory {
            deleteCategory(
                id: self.test_instance.id
            ) {
                success
                message
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['deleteCategory']['success'])
