from rest_framework import serializers
from drf_spectacular.utils import (
    OpenApiParameter,
    inline_serializer,
    extend_schema,
    OpenApiResponse
)
from drf_spectacular.types import OpenApiTypes

total_response_schema = inline_serializer(
    name='TotalResponse',
    fields={
        'total_earned': serializers.DecimalField(max_digits=10, decimal_places=2),
        'total_spent': serializers.DecimalField(max_digits=10, decimal_places=2),
        'net_earnings': serializers.DecimalField(max_digits=10, decimal_places=2),
    },
)

categories_response_schema = inline_serializer(
    name='CategoriesResponse',
    fields={
        'expenses_by_category': serializers.ListField(
            child=inline_serializer(
                name='CategoryExpense',
                fields={
                    'category__name': serializers.CharField(),
                    'total_expenses': serializers.DecimalField(max_digits=10, decimal_places=2),
                },
            )
        )
    },
)

average_response_schema = inline_serializer(
    name='AverageResponse',
    fields={
    '"average_expenses': serializers.ListField(
            child=inline_serializer(
                name='CategoryAverageExpense',
                fields={
                    'category__name': serializers.CharField(),
                    'average_expense': serializers.DecimalField(max_digits=10, decimal_places=2),
                },
            )
        )
    },
)

error_response_schema = inline_serializer(
    name='ErrorResponse',
    fields={
        'error': serializers.CharField(),
        'details': serializers.CharField(required=False),
    },
)

aggregation_schema = extend_schema(
    description=(
        'Dynamic aggregation endpoint for calculating totals, expenses by categories, '
        'and average expenses. Use query parameters to customize the response.\n\n'
        '**Available Query Parameters**:\n'
        '- `type` (required): Determines the type of aggregation. Options are:\n'
        '  - `total`: Returns total earned, total spent, and net earnings.\n'
        '  - `categories`: Returns expenses grouped by categories.\n'
        '  - `average`: Returns average expenses grouped by categories.\n'
        '- `year` (optional): Filter data by a specific year.\n'
        '- `month` (optional): Filter data by a specific month.\n'
        '- `date` (optional): Filter data by a specific date.\n'
        '- `categories` (optional): A list of category IDs to filter expenses.\n\n'
        '**Examples**:\n'
        '- `?type=total&year=2025`: Get total earnings and expenses for the year 2025.\n'
        '- `?type=categories&month=4`: Get expenses grouped by categories for April.\n'
        '- `?type=average&categories=1,2`: Get average expenses for categories 1 and 2.'
    ),
    parameters=[
        OpenApiParameter(
            name='type',
            type=OpenApiTypes.STR,
            description=(
                'The type of aggregation to perform. Options are:\n'
                '- `total`: Total earned, total spent, and net earnings.\n'
                '- `categories`: Expenses grouped by categories.\n'
                '- `average`: Average expenses grouped by categories.'
            ),
            required=True
        ),
        OpenApiParameter(
            name='year',
            type=OpenApiTypes.INT,
            description='Filter data by a specific year (e.g., `2025`).',
            required=False
        ),
        OpenApiParameter(
            name='month',
            type=OpenApiTypes.INT,
            description='Filter data by a specific month (1-12).',
            required=False
        ),
        OpenApiParameter(
            name='date',
            type=OpenApiTypes.DATE,
            description='Filter data by a specific date.',
            required=False
        ),
        OpenApiParameter(
            name='categories',
            type=OpenApiTypes.STR,
            description=(
                'A comma-separated list of category IDs to filter expenses '
                '(e.g., `?categories=1,2,3`).'
            ),
            required=False
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=total_response_schema,
            description="Response for the 'total' aggregation type."
        ),
        200: OpenApiResponse(
            response=categories_response_schema,
            description="Response for the 'categories' aggregation type."
        ),
        200: OpenApiResponse(
            response=average_response_schema,
            description="Response for the 'average' aggregation type."
        ),
        400: OpenApiResponse(
            response=error_response_schema,
            description="Error response for invalid query parameters."
        ),
    }
)

