import json
from django.test import TestCase
from graphene.test import Client
from ..schema import schema
from api import models

class ContactMessageTestCase(TestCase):
    def setUp(self):
        # Create test data here
        self.test_instance = models.ContactMessage.objects.create(
            # Add required fields here, e.g.:
            # field_name='value',
        )

    def test_query_contact_message(self):
        # Test querying ContactMessage
        client = Client(schema)
        query = '''
        query {
            contact_messageList {
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
        self.assertIn('contact_messageList', executed.get('data'))

    def test_create_contact_message(self):
        # Test creating ContactMessage
        client = Client(schema)
        mutation = '''
        mutation CreateContactMessage {
            createContactMessage(
                # Add required fields here, e.g.:
                # field_name: "value"
            ) {
                success
                message
                contact_message {
                    id
                }
                errors
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['createContactMessage']['success'])
        self.assertIsNotNone(executed['data']['createContactMessage'][ContactMessage.lower()]['id'])

    def test_update_contact_message(self):
        # Test updating ContactMessage
        client = Client(schema)
        mutation = '''
        mutation UpdateContactMessage {
            updateContactMessage(
                id: self.test_instance.id,
                # Add fields to update here, e.g.:
                # field_name: "new_value"
            ) {
                success
                message
                contact_message {
                    id
                }
                errors
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['updateContactMessage']['success'])

    def test_delete_contact_message(self):
        # Test deleting ContactMessage
        client = Client(schema)
        mutation = '''
        mutation DeleteContactMessage {
            deleteContactMessage(
                id: self.test_instance.id
            ) {
                success
                message
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['deleteContactMessage']['success'])
