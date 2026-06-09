"""
Middlewares de sécurité SGHL :
- Anti-XSS headers
- Rate limiting HTTP
- Logging des requêtes suspectes
"""
import re
import logging
from django.http import JsonResponse
from django.core.cache import cache

logger = logging.getLogger(__name__)

# Patterns d'injection SQL et XSS basiques
SUSPICIOUS_PATTERNS = [
    re.compile(r'<script[^>]*>', re.IGNORECASE),
    re.compile(r'javascript:', re.IGNORECASE),
    re.compile(r'on\w+\s*=', re.IGNORECASE),
    re.compile(r"(union|select|insert|update|delete|drop|truncate)\s+", re.IGNORECASE),
    re.compile(r"(--|;|'|\"|`)\s*(or|and)\s+", re.IGNORECASE),
]

RATE_LIMIT_PATHS = {
    '/api/v1/auth/login/': (5, 300),    # 5 tentatives / 5 min
    '/api/v1/auth/refresh/': (20, 60),  # 20 / min
}


class SecurityHeadersMiddleware:
    """Ajouter les headers de sécurité à chaque réponse."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        if not response.get('Cache-Control'):
            response['Cache-Control'] = 'no-store'
        return response


class RateLimitMiddleware:
    """Rate limiting par IP sur les endpoints sensibles."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path in RATE_LIMIT_PATHS and request.method == 'POST':
            max_attempts, window = RATE_LIMIT_PATHS[path]
            ip = self._get_ip(request)
            key = f'rl:{path}:{ip}'
            count = cache.get(key, 0)
            if count >= max_attempts:
                logger.warning(f"Rate limit dépassé: {ip} sur {path}")
                return JsonResponse(
                    {'detail': 'Trop de tentatives. Réessayez plus tard.'},
                    status=429
                )
            cache.set(key, count + 1, timeout=window)
        return self.get_response(request)

    @staticmethod
    def _get_ip(request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        return xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR', '')


class InputSanitizationMiddleware:
    """Détecter et bloquer les tentatives d'injection XSS/SQL dans les paramètres GET."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'GET':
            for value in request.GET.values():
                for pattern in SUSPICIOUS_PATTERNS:
                    if pattern.search(value):
                        ip = request.META.get('REMOTE_ADDR', '')
                        logger.warning(f"Tentative d'injection détectée depuis {ip}: {value[:100]}")
                        return JsonResponse({'detail': 'Requête invalide.'}, status=400)
        return self.get_response(request)
