from django.utils.deprecation import MiddlewareMixin
from .services.authentication_service import AuthenticationService
from .services.logger_service import LoggerService

class DynamicRouteGuardMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.auth_service = AuthenticationService()
        self.logger = LoggerService(name='DynamicRouteGuardMiddleware', log_file='middleware.log')
        self.logger.get_logger().debug("DynamicRouteGuardMiddleware initialized")

    def __call__(self, request):
        logger = self.logger.get_logger()
        logger.debug(f"Request path: {request.path}")

        # Process request through authentication service
        response = self.auth_service.process_request(request)
        if response:
            return response

        response = self.get_response(request)
        logger.debug(f"Response status: {response.status_code}")
        return response
