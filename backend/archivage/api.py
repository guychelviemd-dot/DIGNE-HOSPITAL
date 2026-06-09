from ninja import Router, Schema
from typing import List, Optional
from datetime import datetime
from django.shortcuts import get_object_or_404
from .models import DocumentMedical, ArchiveDossier, AccesDocument

router = Router(tags=['Archivage'])


class DocumentOut(Schema):
    id: int
    patient_id: int
    type_document: str
    titre: str
    mime_type: str
    taille_octets: int
    version: int
    created_at: datetime
    acces_patient: bool
    confidentiel: bool


@router.get('/documents/', response=List[DocumentOut])
def list_documents(request, patient_id: Optional[int] = None, type_doc: Optional[str] = None):
    qs = DocumentMedical.objects.select_related('patient')
    if patient_id:
        qs = qs.filter(patient_id=patient_id)
    if type_doc:
        qs = qs.filter(type_document=type_doc)
    return qs


@router.get('/documents/{doc_id}', response=DocumentOut)
def get_document(request, doc_id: int):
    doc = get_object_or_404(DocumentMedical, id=doc_id)
    # Tracer l'accès
    try:
        from personnel.models import Personnel
        personnel = Personnel.objects.get(user=request.user)
        AccesDocument.objects.create(
            document=doc, personnel=personnel, type_acces='Lecture',
            ip_address=request.META.get('REMOTE_ADDR')
        )
    except Exception:
        pass
    return doc


@router.get('/dossier/{patient_id}/archive')
def get_archive(request, patient_id: int):
    archive, _ = ArchiveDossier.objects.get_or_create(patient_id=patient_id)
    return {
        'statut': archive.statut,
        'date_archivage': archive.date_archivage,
        'date_destruction_prevue': archive.date_destruction_prevue,
        'consentement_donne': archive.consentement_donne,
    }
