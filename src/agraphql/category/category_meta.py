create_category = """
# Mutation `createCategory`

This mutation creates a new Category in the system.

## **Parameters:
- `id` (Int) : Id
- `name` (String) : Name
- `slug` (String) : Slug
- `active` (Boolean) : Active
- `metas` (JSONString) : JSON data for metas
- `updated_by` (ID!) : Related User ID
- `added_by` (ID!) : Related User ID
- `status` (Boolean) : Status

## **Returns:
- `success` (Boolean) : Indicates whether the operation was successful
- `message` (String) : Response message indicating success or failure
- `category` (CategoryType) : Created Category object
- `errors` (String) : Error details if operation failed

---

## **Syntax
```graphql
mutation CreateCategory(
    $id: Int
    $name: String
    $slug: String
    $active: Boolean
    $metas: JSONString
    $updated_by: ID!
    $added_by: ID!
    $status: Boolean
) {
    createCategory(
    ) {
        success
        message
        category {
            id
            name
            slug
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

update_category = """
# Mutation `updateCategory`

This mutation updates an existing Category.

## **Parameters:
- `id` (ID!) : Category ID (Required)
- `name` (String) : Name
- `slug` (String) : Slug
- `active` (Boolean) : Active
- `metas` (JSONString) : JSON data for metas
- `updated_by` (ID) : Related User ID
- `added_by` (ID) : Related User ID
- `is_deleted` (Boolean) : Is Deleted
- `status` (Boolean) : Status

## **Returns:
- `success` (Boolean) : Indicates whether the operation was successful
- `message` (String) : Response message indicating success or failure
- `category` (CategoryType) : Updated Category object
- `errors` (String) : Error details if operation failed

---

## **Syntax
```graphql
mutation UpdateCategory(
    $id: ID!
    $name: String
    $slug: String
    $active: Boolean
    $metas: JSONString
    $updated_by: ID
    $added_by: ID
    $is_deleted: Boolean
    $status: Boolean
) {
    updateCategory(
        id: $id
        article: $article
        name: $name
        slug: $slug
        active: $active
        metas: $metas
        updated_by: $updated_by
        added_by: $added_by
        is_deleted: $is_deleted
        status: $status
    ) {
        success
        message
        category {
            id
            name
            slug
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
