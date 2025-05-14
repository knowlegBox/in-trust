import json
from django.test import TestCase
from graphene.test import Client
from ..schema import schema
from api import models

class ProfileTestCase(TestCase):
    def setUp(self):
        # Create test data here
        self.test_instance = models.Profile.objects.create(
            # Add required fields here, e.g.:
            # field_name='value',
        )

    def test_query_profile(self):
        # Test querying Profile
        client = Client(schema)
        query = '''
        query {
            profileList {
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
        self.assertIn('profileList', executed.get('data'))

    def test_create_profile(self):
        # Test creating Profile
        client = Client(schema)
        mutation = '''
        mutation CreateProfile {
            createProfile(
                # Add required fields here, e.g.:
                # field_name: "value"
            ) {
                success
                message
                profile {
                    id
                }
                errors
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['createProfile']['success'])
        self.assertIsNotNone(executed['data']['createProfile'][Profile.lower()]['id'])

    def test_update_profile(self):
        # Test updating Profile
        client = Client(schema)
        mutation = '''
        mutation UpdateProfile {
            updateProfile(
                id: self.test_instance.id,
                # Add fields to update here, e.g.:
                # field_name: "new_value"
            ) {
                success
                message
                profile {
                    id
                }
                errors
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['updateProfile']['success'])

    def test_delete_profile(self):
        # Test deleting Profile
        client = Client(schema)
        mutation = '''
        mutation DeleteProfile {
            deleteProfile(
                id: self.test_instance.id
            ) {
                success
                message
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['deleteProfile']['success'])
