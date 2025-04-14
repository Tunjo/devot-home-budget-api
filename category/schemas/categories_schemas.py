from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from category.serializers import CategorySerializer

categories_schemas = extend_schema_view(
    list=extend_schema(
        description=(
            'Retrieve a list of categories. This includes both user-specific categories '
            'and predefined categories (shared across all users).'
        ),
        responses={200: CategorySerializer(many=True)},
    ),
    create=extend_schema(
        description=(
            'Create a new category. The `user` field is automatically set to the authenticated user.'
        ),
        request=CategorySerializer,
        responses={201: CategorySerializer},
    ),
    update=extend_schema(
        description=(
            'Update an existing category. Predefined categories (shared across all users) '
            'cannot be updated.'
        ),
        request=CategorySerializer,
        responses={200: CategorySerializer},
    ),
    destroy=extend_schema(
        description=(
            'Delete an existing category. Predefined categories (shared across all users) '
            'cannot be deleted.'
        ),
        responses={204: None},
    ),
)