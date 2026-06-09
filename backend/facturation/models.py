from django.db import models
from django.db.models import Sum

class Facture(models.Model):
    STATUT = [('En attente','En attente'),('Partielle','Partielle'),('Payée','Payée'),('Annulée','Annulée')]
    TYPE = [('Consultation','Consultation'),('Hospitalisation','Hospitalisation'),('Examens','Examens'),('Pharmacie','Pharmacie')]

    patient = models.ForeignKey('patients.Patient', on_delete=models.PROTECT, related_name='factures')
    type_facture = models.CharField(max_length=20, choices=TYPE)
    montant_total = models.DecimalField(max_digits=12, decimal_places=2)
    statut = models.CharField(max_length=20, choices=STATUT, default='En attente')
    date_emission = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    @property
    def montant_paye(self):
        return self.paiements.aggregate(total=Sum('montant'))['total'] or 0

    @property
    def solde(self):
        return self.montant_total - self.montant_paye

    def update_statut(self):
        if self.montant_paye >= self.montant_total:
            self.statut = 'Payée'
        elif self.montant_paye > 0:
            self.statut = 'Partielle'
        self.save()

    class Meta:
        ordering = ['-date_emission']

class Paiement(models.Model):
    MODE = [('Espèces','Espèces'),('Mobile Money','Mobile Money'),('Assurance','Assurance'),('Virement','Virement')]
    facture = models.ForeignKey(Facture, on_delete=models.PROTECT, related_name='paiements')
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    mode_paiement = models.CharField(max_length=20, choices=MODE)
    date_paiement = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=100, blank=True)
