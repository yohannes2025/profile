# config/spectacular_hooks.py

def fix_user_m2m_crash(result, generator, **kwargs):
    """
    Post-processing hook that ensures any partial or broken structural components
    generated for auth relationships do not break schema compilation.
    """
    # Prevent nested permission structures from breaking downstream parsing
    if 'schemas' in result.get('components', {}):
        schemas = result['components']['schemas']
        
        # If a User component was partially compiled and crashed, we normalize it here
        if 'User' in schemas:
            properties = schemas['User'].get('properties', {})
            # Safely drop or isolate the fields causing introspective errors
            properties.pop('groups', None)
            properties.pop('user_permissions', None)
            
    return result