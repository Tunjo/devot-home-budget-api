from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from category.serializers import ExpenseSerializer


expense_schema = extend_schema_view(
    list=extend_schema(
        description=(
            'Retrieve a list of expenses with the following options:\n\n'
            '**Filters**:\n'
            '- `min_price`: Filter by an amount greater than or equal to this value.\n'
            '- `max_price`: Filter by an amount less than or equal to this value.\n'
            '- `start_date`: Filter by a date greater than or equal to this value.\n'
            '- `end_date`: Filter by a date less than or equal to this value.\n'
            '- `date`: Filter by an exact date.\n'
            '- `category`: Filter by category name (case-insensitive) or category ID.\n\n'
            '**Search**:\n'
            '- `search`: Search by description or category name.\n\n'
            '**Ordering**:\n'
            '- `ordering`: Order results by a field. Prefix with "-" for descending order. Available fields: `date`, `amount`, `category__name`.\n\n'
            '**Pagination**:\n'
            '- `page`: Page number for pagination.'
        ),
        responses={200: ExpenseSerializer(many=True)},
    ),
    create=extend_schema(
        description=(
            'Create a new expense. The `user` field is automatically set to the authenticated user.\n\n'
            '**Request Body**:\n'
            '- `amount` (required): The amount of the expense.\n'
            '- `description` (optional): A description of the expense.\n'
            '- `category` (required): The ID of the category associated with the expense.\n\n'
            '**Response**:\n'
            'Returns the created expense object with its details.'
        ),
        request=ExpenseSerializer,
        responses={201: ExpenseSerializer},
    ),
    update=extend_schema(
        description=(
            'Update an existing expense. The `user` field cannot be modified.'
        ),
        request=ExpenseSerializer,
        responses={200: ExpenseSerializer},
    ),
    destroy=extend_schema(
        description=(
            'Delete an existing expense.'
        ),
        responses={204: None},
    ),
)