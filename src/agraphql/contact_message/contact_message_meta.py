create_contact_message = """
# Mutation `createContactMessage`

This mutation creates a new ContactMessage in the system.

## **Parameters:
- `id` (Int) : Id
- `name` (String) : Name
- `email` (String) : Email
- `subject` (String) : Subject
- `message` (String) : Message
- `sent_at` (Date) : Sent At
- `is_processed` (Boolean) : Is Processed
- `active` (Boolean) : Active
- `metas` (JSONString) : JSON data for metas
- `updated_by` (ID!) : Related User ID
- `added_by` (ID!) : Related User ID
- `status` (Boolean) : Status

## **Returns:
- `success` (Boolean) : Indicates whether the operation was successful
- `message` (String) : Response message indicating success or failure
- `contact_message` (ContactMessageType) : Created ContactMessage object
- `errors` (String) : Error details if operation failed

---

## **Syntax
```graphql
mutation CreateContactMessage(
    $id: Int
    $name: String
    $email: String
    $subject: String
    $message: String
    $sent_at: Date
    $is_processed: Boolean
    $active: Boolean
    $metas: JSONString
    $updated_by: ID!
    $added_by: ID!
    $status: Boolean
) {
    createContactMessage(
    ) {
        success
        message
        contact_message {
            id
            name
            email
            subject
            message
            sent_at
            is_processed
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

update_contact_message = """
# Mutation `updateContactMessage`

This mutation updates an existing ContactMessage.

## **Parameters:
- `id` (ID!) : ContactMessage ID (Required)
- `name` (String) : Name
- `email` (String) : Email
- `subject` (String) : Subject
- `message` (String) : Message
- `sent_at` (Date) : Sent At
- `is_processed` (Boolean) : Is Processed
- `active` (Boolean) : Active
- `metas` (JSONString) : JSON data for metas
- `updated_by` (ID) : Related User ID
- `added_by` (ID) : Related User ID
- `is_deleted` (Boolean) : Is Deleted
- `status` (Boolean) : Status

## **Returns:
- `success` (Boolean) : Indicates whether the operation was successful
- `message` (String) : Response message indicating success or failure
- `contact_message` (ContactMessageType) : Updated ContactMessage object
- `errors` (String) : Error details if operation failed

---

## **Syntax
```graphql
mutation UpdateContactMessage(
    $id: ID!
    $name: String
    $email: String
    $subject: String
    $message: String
    $sent_at: Date
    $is_processed: Boolean
    $active: Boolean
    $metas: JSONString
    $updated_by: ID
    $added_by: ID
    $is_deleted: Boolean
    $status: Boolean
) {
    updateContactMessage(
        id: $id
        name: $name
        email: $email
        subject: $subject
        message: $message
        sent_at: $sent_at
        is_processed: $is_processed
        active: $active
        metas: $metas
        updated_by: $updated_by
        added_by: $added_by
        is_deleted: $is_deleted
        status: $status
    ) {
        success
        message
        contact_message {
            id
            name
            email
            subject
            message
            sent_at
            is_processed
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
