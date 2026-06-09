from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from ninja import NinjaAPI
from ninja.security import HttpBearer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            from rest_framework_simplejwt.tokens import AccessToken
            from django.contrib.auth.models import User
            # Décoder le jeton
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            # Récupérer l'utilisateur
            user = User.objects.get(id=user_id)
            # Injecter dans request
            request.user = user
            request.user_id = user.id
            request.user_email = user.email
            return token
        except Exception:
            return None

api = NinjaAPI(version='1.0', title='SGHL API', auth=JWTAuth())

from patients.api import router as patients_router
from hospitalisations.api import router as hospit_router
from laboratoire.api import router as labo_router
from pharmacie.api import router as pharma_router
from facturation.api import router as factu_router
from personnel.api import router as personnel_router
from audit.api import router as audit_router
from dashboard.api import router as dashboard_router
from soins.api import router as soins_router
from chat.api import router as chat_router
from gardes.api import router as gardes_router
from rendez_vous.api import router as rdv_router
from prescriptions.api import router as prescriptions_router
from consentement.api import router as consentement_router
from urgences.api import router as urgences_router
from imagerie.api import router as imagerie_router
from bloc_operatoire.api import router as bloc_router
from maternite.api import router as maternite_router
from teleconsultation.api import router as teleconsult_router
from archivage.api import router as archivage_router
from interoperabilite.api import router as fhir_router

api.add_router('/patients/', patients_router)
api.add_router('/hospitalisations/', hospit_router)
api.add_router('/laboratoire/', labo_router)
api.add_router('/pharmacie/', pharma_router)
api.add_router('/facturation/', factu_router)
api.add_router('/personnel/', personnel_router)
api.add_router('/audit/', audit_router)
api.add_router('/dashboard/', dashboard_router)
api.add_router('/soins/', soins_router)
api.add_router('/chat/', chat_router)
api.add_router('/gardes/', gardes_router)
api.add_router('/rendez-vous/', rdv_router)
api.add_router('/prescriptions/', prescriptions_router)
api.add_router('/consentement/', consentement_router)
api.add_router('/urgences/', urgences_router)
api.add_router('/imagerie/', imagerie_router)
api.add_router('/bloc-operatoire/', bloc_router)
api.add_router('/maternite/', maternite_router)
api.add_router('/teleconsultation/', teleconsult_router)
api.add_router('/archivage/', archivage_router)
api.add_router('/interop/', fhir_router)

def sante_view(request):
    """Endpoint de health check enrichi."""
    from django.utils import timezone
    checks = {'status': 'ok', 'timestamp': timezone.now().isoformat(), 'version': '1.0'}
    # DB
    try:
        from django.db import connection
        connection.ensure_connection()
        checks['database'] = 'ok'
    except Exception as e:
        checks['database'] = f'error: {e}'
        checks['status'] = 'degraded'
    # Cache/Redis
    try:
        from django.core.cache import cache
        cache.set('_health', '1', 5)
        checks['cache'] = 'ok' if cache.get('_health') else 'miss'
    except Exception as e:
        checks['cache'] = f'error: {e}'
        checks['status'] = 'degraded'
    # Counts
    try:
        from patients.models import Patient
        from hospitalisations.models import Hospitalisation
        checks['patients_total'] = Patient.objects.count()
        checks['hospitalisations_actives'] = Hospitalisation.objects.filter(statut='Actif').count()
    except Exception:
        pass
    status_code = 200 if checks['status'] == 'ok' else 503
    return JsonResponse(checks, status=status_code)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', api.urls),
    path('api/v1/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/sante/', sante_view, name='sante'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
