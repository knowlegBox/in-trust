create_newsletter_subscriber = """
# Mutation `createNewsletterSubscriber`

This mutation creates a new NewsletterSubscriber in the system.

## **Parameters:
- `id` (Int) : Id
- `email` (String) : Email
- `subscribed_at` (Date) : Subscribed At
- `is_confirmed` (Boolean) : Is Confirmed
- `confirmation_token` (String) : Confirmation Token
- `active` (Boolean) : Active
- `metas` (JSONString) : JSON data for metas
- `updated_by` (ID!) : Related User ID
- `added_by` (ID!) : Related User ID
- `status` (Boolean) : Status

## **Returns:
- `success` (Boolean) : Indicates whether the operation was successful
- `message` (String) : Response message indicating success or failure
- `newsletter_subscriber` (NewsletterSubscriberType) : Created NewsletterSubscriber object
- `errors` (String) : Error details if operation failed

---

## **Syntax
```graphql
mutation CreateNewsletterSubscriber(
    $id: Int
    $email: String
    $subscribed_at: Date
    $is_confirmed: Boolean
    $confirmation_token: String
    $active: Boolean
    $metas: JSONString
    $updated_by: ID!
    $added_by: ID!
    $status: Boolean
) {
    createNewsletterSubscriber(
    ) {
        success
        message
        newsletter_subscriber {
            id
            email
            subscribed_at
            is_confirmed
            confirmation_token
            active
            metas
            created_at
            updated_by
            added_by
            is_deleted
            status
        }
        errors
    }
}
```"""

update_newsletter_subscriber = """
# Mutation `updateNewsletterSubscriber`

This mutation updates an existing NewsletterSubscriber.

## **Parameters:
- `id` (ID!) : NewsletterSubscriber ID (Required)
- `email` (String) : Email
- `subscribed_at` (Date) : Subscribed At
- `is_confirmed` (Boolean) : Is Confirmed
- `confirmation_token` (String) : Confirmation Token
- `active` (Boolean) : Active
- `metas` (JSONString) : JSON data for metas
- `updated_by` (ID) : Related User ID
- `added_by` (ID) : Related User ID
- `is_deleted` (Boolean) : Is Deleted
- `status` (Boolean) : Status

## **Returns:
- `success` (Boolean) : Indicates whether the operation was successful
- `message` (String) : Response message indicating success or failure
- `newsletter_subscriber` (NewsletterSubscriberType) : Updated NewsletterSubscriber object
- `errors` (String) : Error details if operation failed

---

## **Syntax
```graphql
mutation UpdateNewsletterSubscriber(
    $id: ID!
    $email: String
    $subscribed_at: Date
    $is_confirmed: Boolean
    $confirmation_token: String
    $active: Boolean
    $metas: JSONString
    $updated_by: ID
    $added_by: ID
    $is_deleted: Boolean
    $status: Boolean
) {
    updateNewsletterSubscriber(
        id: $id
        email: $email
        subscribed_at: $subscribed_at
        is_confirmed: $is_confirmed
        confirmation_token: $confirmation_token
        active: $active
        metas: $metas
        updated_by: $updated_by
        added_by: $added_by
        is_deleted: $is_deleted
        status: $status
    ) {
        success
        message
        newsletter_subscriber {
            id
            email
            subscribed_at
            is_confirmed
            confirmation_token
            active
            metas
            created_at
            updated_by
            added_by
            is_deleted
            status
        }
        errors
    }
}
```"""
