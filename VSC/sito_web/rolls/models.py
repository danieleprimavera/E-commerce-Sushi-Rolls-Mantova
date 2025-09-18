from django.db import models
from django.contrib.auth.models import User

# crea i modelli per il database 
class Roll(models.Model):
    nome = models.CharField(max_length=20)
    prezzo = models.FloatField()
    immagine = models.ImageField()
    class Meta:
        verbose_name = "Prodotto"
        verbose_name_plural = "Prodotti"

    def __str__(self):
        return self.nome

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    data_nascita = models.DateField(null=True, blank=True)
    class Meta:
        verbose_name = "Utente registrato"
        verbose_name_plural = "Utenti registrati"

    def __str__(self):
        return f"Profilo di {self.user.username}"


class Ordine(models.Model):
    METODI_PAGAMENTO = [
        ("visa", "Visa"),
        ("mastercard", "Mastercard"),
        ("paypal", "PayPal"),
        ("klarna", "Klarna"),
    ]
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ordini")
    indirizzo_spedizione = models.CharField(max_length=255)
    metodo_pagamento = models.CharField(max_length=20, choices=METODI_PAGAMENTO)
    data = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Ordine effettuato"
        verbose_name_plural = "Ordini effettuati"

    def totale(self):
        return sum(item.prezzo_unitario * item.quantita for item in self.items.all())

    def __str__(self):
        return f"Ordine #{self.id} di {self.cliente.username} - {self.data:%Y-%m-%d}"


class OrdineItem(models.Model):
    ordine = models.ForeignKey(Ordine, on_delete=models.CASCADE, related_name="items")
    roll = models.ForeignKey(Roll, on_delete=models.PROTECT)
    prezzo_unitario = models.FloatField()
    quantita = models.PositiveIntegerField(default=1)

    def subtotale(self):
        return self.prezzo_unitario * self.quantita

    def __str__(self):
        return f"{self.roll.nome} x {self.quantita}"
    
class Contatto(models.Model):
    email = models.EmailField()
    messaggio = models.TextField()
    data_invio = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Messaggio del cliente"
        verbose_name_plural = "Messaggi dei clienti"

    def __str__(self):
        return f"{self.email} - {self.data_invio.strftime('%d/%m/%Y %H:%M')}"
