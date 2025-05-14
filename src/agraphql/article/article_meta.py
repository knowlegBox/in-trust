create_article = """
# Mutation `createArticle`

This mutation creates a new Article in the system.

## **Parameters:
- `id` (Int) : Id
- `title` (String) : Title
- `slug` (String) : Slug
- `author` (ID!) : Related User ID
- `content` (String) : Content
- `is_private` (Boolean) : Is Private
- `active` (Boolean) : Active
- `metas` (JSONString) : JSON data for metas
- `updated_by` (ID!) : Related User ID
- `added_by` (ID!) : Related User ID
- `status` (Boolean) : Status

## **Returns:
- `success` (Boolean) : Indicates whether the operation was successful
- `message` (String) : Response message indicating success or failure
- `article` (ArticleType) : Created Article object
- `errors` (String) : Error details if operation failed

---

## **Syntax
```graphql
mutation CreateArticle(
    $id: Int
    $title: String
    $slug: String
    $author: ID!
    $content: String
    $is_private: Boolean
    $active: Boolean
    $metas: JSONString
    $updated_by: ID!
    $added_by: ID!
    $status: Boolean
) {
    createArticle(
    ) {
        success
        message
        article {
            id
            title
            slug
            author
            content
            created_at
            updated_at
            is_private
            active
            metas
            updated_by
            added_by
            is_deleted
            status
            categories
            tags
        }
        errors
    }
}
```"""

update_article = """
# Mutation `updateArticle`

This mutation updates an existing Article.

## **Parameters:
- `id` (ID!) : Article ID (Required)
- `title` (String) : Title
- `slug` (String) : Slug
- `author` (ID) : Related User ID
- `content` (String) : Content
- `is_private` (Boolean) : Is Private
- `active` (Boolean) : Active
- `metas` (JSONString) : JSON data for metas
- `updated_by` (ID) : Related User ID
- `added_by` (ID) : Related User ID
- `is_deleted` (Boolean) : Is Deleted
- `status` (Boolean) : Status

## **Returns:
- `success` (Boolean) : Indicates whether the operation was successful
- `message` (String) : Response message indicating success or failure
- `article` (ArticleType) : Updated Article object
- `errors` (String) : Error details if operation failed

---

## **Syntax
```graphql
mutation UpdateArticle(
    $id: ID!
    $title: String
    $slug: String
    $author: ID
    $content: String
    $is_private: Boolean
    $active: Boolean
    $metas: JSONString
    $updated_by: ID
    $added_by: ID
    $is_deleted: Boolean
    $status: Boolean
) {
    updateArticle(
        id: $id
        title: $title
        slug: $slug
        author: $author
        content: $content
        is_private: $is_private
        active: $active
        metas: $metas
        updated_by: $updated_by
        added_by: $added_by
        is_deleted: $is_deleted
        status: $status
        categories: $categories
        tags: $tags
    ) {
        success
        message
        article {
            id
            title
            slug
            author
            content
            created_at
            updated_at
            is_private
            active
            metas
            updated_by
            added_by
            is_deleted
            status
            categories
            tags
        }
        errors
    }
}
```"""
