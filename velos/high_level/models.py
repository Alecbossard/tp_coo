from django.db import models


class Pays(models.Model):
    nom = models.CharField(max_length=100)
    tva = models.DecimalField(max_digits=5, decimal_places=2)
    tarif_electrique = models.DecimalField(max_digits=10, decimal_places=3)
    salaire_minimum = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nom


class Ville(models.Model):
    nom = models.CharField(max_length=100)
    taxe_immobiliere = models.DecimalField(max_digits=10, decimal_places=2)
    prix_m2 = models.DecimalField(max_digits=10, decimal_places=2)
    pays = models.ForeignKey(Pays, on_delete=models.PROTECT)

    def __str__(self):
        return self.nom


class Machine(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=12, decimal_places=2)
    duree_de_vie = models.IntegerField()
    cout_maintenance = models.DecimalField(max_digits=10, decimal_places=2)
    superficie = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nom


class QuantiteMachine(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT)
    nombre = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} x {self.machine.nom}"


class Lieu(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.ForeignKey(Ville, on_delete=models.PROTECT)
    superficie = models.DecimalField(max_digits=10, decimal_places=2)
    quantite_machines = models.ManyToManyField(QuantiteMachine)
    consommation_electrique = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nom


class Transport(models.Model):
    nombre_palettes = models.IntegerField()
    cout = models.DecimalField(max_digits=10, decimal_places=2)
    delai = models.IntegerField()
    depart = models.ForeignKey(
        Lieu,
        on_delete=models.PROTECT,
        related_name="transports_depart",
    )
    arrivee = models.ForeignKey(
        Lieu,
        on_delete=models.PROTECT,
        related_name="transports_arrivee",
    )

    def __str__(self):
        return f"{self.depart} vers {self.arrivee}"


class Operation(models.Model):
    nom = models.CharField(max_length=100)
    operation_suivante = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="operations_precedentes",
    )
    cout = models.DecimalField(max_digits=10, decimal_places=2)
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT)
    quantite_produits = models.ManyToManyField("QuantiteProduit")
    heures_de_travail = models.DecimalField(max_digits=10, decimal_places=2)
    consommation_electrique = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=100)
    prix_de_vente = models.DecimalField(max_digits=10, decimal_places=2)
    duree_de_vie = models.IntegerField()
    nombre_par_palette = models.IntegerField()
    operations = models.ManyToManyField(Operation)

    def __str__(self):
        return self.nom


class PrixProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.produit.nom} - {self.prix_achat}"


class QuantiteProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    nombre = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} x {self.produit.nom}"


class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    prix_produits = models.ManyToManyField(PrixProduit)

    def __str__(self):
        return self.nom


class Stock(models.Model):
    quantite_produits = models.ManyToManyField(QuantiteProduit)
    palettes_max = models.IntegerField()

    def __str__(self):
        return f"Stock (max {self.palettes_max} palettes)"


class PointDeVente(models.Model):
    nom = models.CharField(max_length=100)
    lieu = models.ForeignKey(Lieu, on_delete=models.PROTECT)
    heures_de_travail = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)

    def __str__(self):
        return self.nom


class Facture(models.Model):
    quantite_produits = models.ManyToManyField(QuantiteProduit)
    reduction = models.DecimalField(max_digits=5, decimal_places=2)
    point_de_vente = models.ForeignKey(
        PointDeVente,
        on_delete=models.PROTECT,
    )
    client = models.CharField(max_length=100)

    def __str__(self):
        return f"Facture {self.pk} - {self.client}"
