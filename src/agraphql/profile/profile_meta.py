create_profile = """
# Mutation `createProfile`

This mutation creates a new Profile in the system.

## **Parameters:
- `id` (Int) : Id
- `user` (ID!) : Related User ID
- `avatar` (String) : Avatar
- `bio` (String) : Bio
- `active` (Boolean) : Active
- `metas` (JSONString) : JSON data for metas
- `updated_by` (ID!) : Related User ID
- `added_by` (ID!) : Related User ID
- `status` (Boolean) : Status

## **Returns:
- `success` (Boolean) : Indicates whether the operation was successful
- `message` (String) : Response message indicating success or failure
- `profile` (ProfileType) : Created Profile object
- `errors` (String) : Error details if operation failed

---

## **Syntax
```graphql
mutation CreateProfile(
    $id: Int
    $user: ID!
    $avatar: String
    $bio: String
    $active: Boolean
    $metas: JSONString
    $updated_by: ID!
    $added_by: ID!
    $status: Boolean
) {
    createProfile(
    ) {
        success
        message
        profile {
            id
            user
            avatar
            bio
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

update_profile = """
# Mutation `updateProfile`

This mutation updates an existing Profile.

## **Parameters:
- `id` (ID!) : Profile ID (Required)
- `user` (ID) : Related User ID
- `avatar` (String) : Avatar
- `bio` (String) : Bio
- `active` (Boolean) : Active
- `metas` (JSONString) : JSON data for metas
- `updated_by` (ID) : Related User ID
- `added_by` (ID) : Related User ID
- `is_deleted` (Boolean) : Is Deleted
- `status` (Boolean) : Status

## **Returns:
- `success` (Boolean) : Indicates whether the operation was successful
- `message` (String) : Response message indicating success or failure
- `profile` (ProfileType) : Updated Profile object
- `errors` (String) : Error details if operation failed

---

## **Syntax
```graphql
mutation UpdateProfile(
    $id: ID!
    $user: ID
    $avatar: String
    $bio: String
    $active: Boolean
    $metas: JSONString
    $updated_by: ID
    $added_by: ID
    $is_deleted: Boolean
    $status: Boolean
) {
    updateProfile(
        id: $id
        user: $user
        avatar: $avatar
        bio: $bio
        active: $active
        metas: $metas
        updated_by: $updated_by
        added_by: $added_by
        is_deleted: $is_deleted
        status: $status
    ) {
        success
        message
        profile {
            id
            user
            avatar
            bio
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
