# users/apps.py
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from rest_framework.utils import model_meta
        from collections import OrderedDict
        from rest_framework.utils.model_meta import RelationInfo

        def bulletproof_get_forward_relationships(opts):
            """
            Completely replaces the DRF model_meta function with an 
            AttributeError firewall across all relational lookups.
            """
            forward_relations = OrderedDict()
            
            # Look at all fields defined on the model option layer
            for field in opts.get_fields():
                if not field.is_relation:
                    continue

                if field.many_to_one or field.one_to_one:
                    forward_relations[field.name] = RelationInfo(
                        model_field=field,
                        related_model=field.remote_field.model,
                        to_many=False,
                        to_field=getattr(field.remote_field, 'field_name', None),
                        has_through_model=False,
                        reverse=False
                    )
                
                elif field.many_to_many:
                    # --- THE FIREWALL CHECK ---
                    # If Django's internal state machine or a package model yields 
                    # a missing or incomplete through model reference, intercept it cleanly.
                    has_through = False
                    if hasattr(field, 'remote_field') and field.remote_field:
                        through_attr = getattr(field.remote_field, 'through', None)
                        if through_attr and hasattr(through_attr, '_meta') and through_attr._meta:
                            has_through = not through_attr._meta.auto_created
                    
                    forward_relations[field.name] = RelationInfo(
                        model_field=field,
                        related_model=field.remote_field.model,
                        to_many=True,
                        to_field=None,
                        has_through_model=has_through,
                        reverse=False
                    )

            return forward_relations

        # Overwrite the Django REST Framework utility function entirely
        model_meta._get_forward_relationships = bulletproof_get_forward_relationships