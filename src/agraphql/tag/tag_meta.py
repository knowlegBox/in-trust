create_tag = """
# Mutation `createTag`

This mutation creates a new Tag in the system.

## **Parameters:
- `id` (Int) : Id
- `name` (String) : Name
- `active` (Boolean) : Active
- `metas` (JSONString) : JSON data for metas
- `updated_by` (ID!) : Related User ID
- `added_by` (ID!) : Related User ID
- `status` (Boolean) : Status

## **Returns:
- `success` (Boolean) : Indicates whether the operation was successful
- `message` (String) : Response message indicating success or failure
- `tag` (TagType) : Created Tag object
- `errors` (String) : Error details if operation failed

---

## **Syntax
```graphql
mutation CreateTag(
    $id: Int
    $name: String
    $active: Boolean
    $metas: JSONString
    $updated_by: ID!
    $added_by: ID!
    $status: Boolean
) {
    createTag(
    ) {
        success
        message
        tag {
            id
            name
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

update_tag = """
# Mutation `updateTag`

This mutation updates an existing Tag.

## **Parameters:
- `id` (ID!) : Tag ID (Required)
- `name` (String) : Name
- `active` (Boolean) : Active
- `metas` (JSONString) : JSON data for metas
- `updated_by` (ID) : Related User ID
- `added_by` (ID) : Related User ID
- `is_deleted` (Boolean) : Is Deleted
- `status` (Boolean) : Status

## **Returns:
- `success` (Boolean) : Indicates whether the operation was successful
- `message` (String) : Response message indicating success or failure
- `tag` (TagType) : Updated Tag object
- `errors` (String) : Error details if operation failed

---

## **Syntax
```graphql
mutation UpdateTag(
    $id: ID!
    $name: String
    $active: Boolean
    $metas: JSONString
    $updated_by: ID
    $added_by: ID
    $is_deleted: Boolean
    $status: Boolean
) {
    updateTag(
        id: $id
        article: $article
        name: $name
        active: $active
        metas: $metas
        updated_by: $updated_by
        added_by: $added_by
        is_deleted: $is_deleted
        status: $status
    ) {
        success
        message
        tag {
            id
            name
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
