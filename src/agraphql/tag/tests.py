import json
from django.test import TestCase
from graphene.test import Client
from ..schema import schema
from api import models

class TagTestCase(TestCase):
    def setUp(self):
        # Create test data here
        self.test_instance = models.Tag.objects.create(
            # Add required fields here, e.g.:
            # field_name='value',
        )

    def test_query_tag(self):
        # Test querying Tag
        client = Client(schema)
        query = '''
        query {
            tagList {
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
        self.assertIn('tagList', executed.get('data'))

    def test_create_tag(self):
        # Test creating Tag
        client = Client(schema)
        mutation = '''
        mutation CreateTag {
            createTag(
                # Add required fields here, e.g.:
                # field_name: "value"
            ) {
                success
                message
                tag {
                    id
                }
                errors
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['createTag']['success'])
        self.assertIsNotNone(executed['data']['createTag'][Tag.lower()]['id'])

    def test_update_tag(self):
        # Test updating Tag
        client = Client(schema)
        mutation = '''
        mutation UpdateTag {
            updateTag(
                id: self.test_instance.id,
                # Add fields to update here, e.g.:
                # field_name: "new_value"
            ) {
                success
                message
                tag {
                    id
                }
                errors
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['updateTag']['success'])

    def test_delete_tag(self):
        # Test deleting Tag
        client = Client(schema)
        mutation = '''
        mutation DeleteTag {
            deleteTag(
                id: self.test_instance.id
            ) {
                success
                message
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['deleteTag']['success'])
