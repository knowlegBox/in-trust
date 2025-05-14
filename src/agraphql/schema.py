import graphene
from graphene import ObjectType

# Import all queries and mutations
from .article import mutations as article_mutations,queries as article_queries,article_meta  
from .category import mutations as category_mutations,queries as category_queries,category_meta  
from .tag import mutations as tag_mutations,queries as tag_queries,tag_meta  
from .news import mutations as news_mutations,queries as news_queries,news_meta  
from .profile import mutations as profile_mutations,queries as profile_queries,profile_meta  
from .newsletter_subscriber import mutations as newsletter_subscriber_mutations,queries as newsletter_subscriber_queries,newsletter_subscriber_meta  
from .contact_message import mutations as contact_message_mutations,queries as contact_message_queries,contact_message_meta  


class Query(article_queries.ArticleQuery, category_queries.CategoryQuery, tag_queries.TagQuery, news_queries.NewsQuery, profile_queries.ProfileQuery, newsletter_subscriber_queries.NewsletterSubscriberQuery, contact_message_queries.ContactMessageQuery, ObjectType):
    pass

class Mutation(ObjectType):
    create_article = article_mutations.CreateArticle.Field(description=article_meta.create_article)
    update_article = article_mutations.UpdateArticle.Field(description=article_meta.update_article)
    delete_article = article_mutations.DeleteArticle.Field()
    create_category = category_mutations.CreateCategory.Field(description=category_meta.create_category)
    update_category = category_mutations.UpdateCategory.Field(description=category_meta.update_category)
    delete_category = category_mutations.DeleteCategory.Field()
    create_tag = tag_mutations.CreateTag.Field(description=tag_meta.create_tag)
    update_tag = tag_mutations.UpdateTag.Field(description=tag_meta.update_tag)
    delete_tag = tag_mutations.DeleteTag.Field()
    create_news = news_mutations.CreateNews.Field(description=news_meta.create_news)
    update_news = news_mutations.UpdateNews.Field(description=news_meta.update_news)
    delete_news = news_mutations.DeleteNews.Field()
    create_profile = profile_mutations.CreateProfile.Field(description=profile_meta.create_profile)
    update_profile = profile_mutations.UpdateProfile.Field(description=profile_meta.update_profile)
    delete_profile = profile_mutations.DeleteProfile.Field()
    create_newsletter_subscriber = newsletter_subscriber_mutations.CreateNewsletterSubscriber.Field(description=newsletter_subscriber_meta.create_newsletter_subscriber)
    update_newsletter_subscriber = newsletter_subscriber_mutations.UpdateNewsletterSubscriber.Field(description=newsletter_subscriber_meta.update_newsletter_subscriber)
    delete_newsletter_subscriber = newsletter_subscriber_mutations.DeleteNewsletterSubscriber.Field()
    create_contact_message = contact_message_mutations.CreateContactMessage.Field(description=contact_message_meta.create_contact_message)
    update_contact_message = contact_message_mutations.UpdateContactMessage.Field(description=contact_message_meta.update_contact_message)
    delete_contact_message = contact_message_mutations.DeleteContactMessage.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
