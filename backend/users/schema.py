# users/schema.py
from drf_spectacular.extensions import OpenApiSerializerExtension
from drf_spectacular.utils import OpenApiBlueprint
from .serializers import UserSerializer, UserProfileSerializer

class HideAuthFieldsUserExtension(OpenApiSerializerExtension):
    target_class = UserSerializer
    match_subclasses = True

    def map_serializer(self, auto_schema, direction):
        schema = auto_schema._map_serializer(self.target_class, direction)
        if schema and 'properties' in schema:
            # Explicitly eliminate fields from ever triggering internal schema lookups
            schema['properties'].pop('groups', None)
            schema['properties'].pop('user_permissions', None)
        return schema