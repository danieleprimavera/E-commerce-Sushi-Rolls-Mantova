from django.contrib import admin
from .models import Roll, Profile, Ordine, OrdineItem
from django.utils.timezone import localtime
from .models import Contatto

@admin.register(Roll)
class RollAdmin(admin.ModelAdmin):
    list_display = ("nome", "prezzo")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("get_nome", "get_cognome", "get_email", "data_nascita", "get_data_registrazione")
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email")

    def get_nome(self, obj): return obj.user.first_name
    get_nome.short_description = "Nome"
    def get_cognome(self, obj): return obj.user.last_name
    get_cognome.short_description = "Cognome"
    def get_email(self, obj): return obj.user.email
    get_email.short_description = "Email"
    def get_data_registrazione(self, obj): return obj.user.date_joined
    get_data_registrazione.short_description = "Data registrazione"

class OrdineItemInline(admin.TabularInline):
    model = OrdineItem
    extra = 0
    readonly_fields = ("roll", "prezzo_unitario", "quantita")
    can_delete = False

@admin.register(Ordine)
class OrdineAdmin(admin.ModelAdmin):
    list_display = ("cliente_nome", "cliente_cognome", "cliente_email", "prodotti_formattati", "indirizzo_spedizione", "metodo_pagamento", "data_locale")
    inlines = [OrdineItemInline]

    def cliente_nome(self, obj): return obj.cliente.first_name
    def cliente_cognome(self, obj): return obj.cliente.last_name
    def cliente_email(self, obj): return obj.cliente.email
    cliente_nome.short_description = "Nome cliente"
    cliente_cognome.short_description = "Cognome cliente"
    cliente_email.short_description = "Email cliente"

    def prodotti_formattati(self, obj):
        parts = []
        for item in obj.items.all():
            parts.append(f"{item.roll.nome} — €{item.prezzo_unitario:.2f} x {item.quantita} = €{item.subtotale():.2f}")
        return " | ".join(parts) if parts else "-"
    prodotti_formattati.short_description = "Prodotti acquistati"

    # FUNZIONE PER ORARIO LOCALE
    def data_locale(self, obj):
        return localtime(obj.data).strftime('%d/%m/%Y %H:%M:%S')
    data_locale.admin_order_field = 'data'
    data_locale.short_description = 'Data e Ora'

@admin.register(Contatto)
class ContattoAdmin(admin.ModelAdmin):
    list_display = ("email", "messaggio_preview", "data_locale")
    search_fields = ("email", "messaggio")
    ordering = ("-data_invio",)

    def messaggio_preview(self, obj):
        # Mostra solo i primi 50 caratteri del messaggio
        return obj.messaggio[:50] + ("..." if len(obj.messaggio) > 50 else "")
    messaggio_preview.short_description = "Messaggio"

    def data_locale(self, obj):
        from django.utils.timezone import localtime
        return localtime(obj.data_invio).strftime('%d/%m/%Y %H:%M:%S')
    data_locale.admin_order_field = "data_invio"
    data_locale.short_description = "Data e Ora"
