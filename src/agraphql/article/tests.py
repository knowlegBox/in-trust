import json
from django.test import TestCase
from graphene.test import Client
from ..schema import schema
from api import models

class ArticleTestCase(TestCase):
    def setUp(self):
        # Create test data here
        self.test_instance = models.Article.objects.create(
            # Add required fields here, e.g.:
            # field_name='value',
        )

    def test_query_article(self):
        # Test querying Article
        client = Client(schema)
        query = '''
        query {
            articleList {
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
        self.assertIn('articleList', executed.get('data'))

    def test_create_article(self):
        # Test creating Article
        client = Client(schema)
        mutation = '''
        mutation CreateArticle {
            createArticle(
                # Add required fields here, e.g.:
                # field_name: "value"
            ) {
                success
                message
                article {
                    id
                }
                errors
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['createArticle']['success'])
        self.assertIsNotNone(executed['data']['createArticle'][Article.lower()]['id'])

    def test_update_article(self):
        # Test updating Article
        client = Client(schema)
        mutation = '''
        mutation UpdateArticle {
            updateArticle(
                id: self.test_instance.id,
                # Add fields to update here, e.g.:
                # field_name: "new_value"
            ) {
                success
                message
                article {
                    id
                }
                errors
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['updateArticle']['success'])

    def test_delete_article(self):
        # Test deleting Article
        client = Client(schema)
        mutation = '''
        mutation DeleteArticle {
            deleteArticle(
                id: self.test_instance.id
            ) {
                success
                message
            }
        }
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['deleteArticle']['success'])
