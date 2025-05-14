create_news = """
# Mutation `createNews`

This mutation creates a new News in the system.

## **Parameters:
- `id` (Int) : Id
- `title` (String) : Title
- `image_url` (String) : Image Url
- `content` (String) : Content
- `category` (String) : Category
- `source_url` (String) : Source Url
- `active` (Boolean) : Active
- `metas` (JSONString) : JSON data for metas
- `updated_by` (ID!) : Related User ID
- `added_by` (ID!) : Related User ID
- `status` (Boolean) : Status

## **Returns:
- `success` (Boolean) : Indicates whether the operation was successful
- `message` (String) : Response message indicating success or failure
- `news` (NewsType) : Created News object
- `errors` (String) : Error details if operation failed

---

## **Syntax
```graphql
mutation CreateNews(
    $id: Int
    $title: String
    $image_url: String
    $content: String
    $category: String
    $source_url: String
    $active: Boolean
    $metas: JSONString
    $updated_by: ID!
    $added_by: ID!
    $status: Boolean
) {
    createNews(
    ) {
        success
        message
        news {
            id
            title
            image_url
            content
            created_at
            category
            source_url
            active
            metas
            updated_by
            added_by
            is_deleted
            status
        }
        errors
    }
}
```"""

update_news = """
# Mutation `updateNews`

This mutation updates an existing News.

## **Parameters:
- `id` (ID!) : News ID (Required)
- `title` (String) : Title
- `image_url` (String) : Image Url
- `content` (String) : Content
- `category` (String) : Category
- `source_url` (String) : Source Url
- `active` (Boolean) : Active
- `metas` (JSONString) : JSON data for metas
- `updated_by` (ID) : Related User ID
- `added_by` (ID) : Related User ID
- `is_deleted` (Boolean) : Is Deleted
- `status` (Boolean) : Status

## **Returns:
- `success` (Boolean) : Indicates whether the operation was successful
- `message` (String) : Response message indicating success or failure
- `news` (NewsType) : Updated News object
- `errors` (String) : Error details if operation failed

---

## **Syntax
```graphql
mutation UpdateNews(
    $id: ID!
    $title: String
    $image_url: String
    $content: String
    $category: String
    $source_url: String
    $active: Boolean
    $metas: JSONString
    $updated_by: ID
    $added_by: ID
    $is_deleted: Boolean
    $status: Boolean
) {
    updateNews(
        id: $id
        title: $title
        image_url: $image_url
        content: $content
        category: $category
        source_url: $source_url
        active: $active
        metas: $metas
        updated_by: $updated_by
        added_by: $added_by
        is_deleted: $is_deleted
        status: $status
    ) {
        success
        message
        news {
            id
            title
            image_url
            content
            created_at
            category
            source_url
            active
            metas
            updated_by
            added_by
            is_deleted
            status
        }
        errors
    }
}
```"""
