from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class SafeAnonRateThrottle(AnonRateThrottle):
    def allow_request(self, request, view):
        # If Render is checking our health, completely bypass the limit
        if request.path == '/healthz':
            return True
        return super().allow_request(request, view)

class SafeUserRateThrottle(UserRateThrottle):
    def allow_request(self, request, view):
        if request.path == '/healthz':
            return True
        return super().allow_request(request, view)