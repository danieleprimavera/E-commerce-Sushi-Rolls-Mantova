from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Roll, Ordine, OrdineItem
from .models import Contatto

def rolls(request):
    rolls = Roll.objects.all()
    return render(request, 'rolls/sushi-rolls.html', {'rolls': rolls})

def search(request):
    query = request.GET.get("q", "").strip().lower()
    results = Roll.objects.none()

    if query:
        # Rimuovo "roll" dalla query se presente
        terms = [t for t in query.split() if t != "roll"]
        results = Roll.objects.all()
        for term in terms:
            results = results.filter(nome__icontains=term)
    
    return render(request, "rolls/search_results.html", {"query": query, "results": results})

@login_required(login_url="login")
def add_to_cart(request, roll_id):
    cart = request.session.get("cart", {})

    # Se il prodotto esiste già, incremento la quantità
    if str(roll_id) in cart:
        cart[str(roll_id)] += 1
    else:
        cart[str(roll_id)] = 1

    request.session["cart"] = cart
    return redirect("carrello")

def contattaci(request):
    if request.method == "POST":
        email = request.POST.get("email")
        messaggio = request.POST.get("messaggio")

        # Salva il contatto nel database
        Contatto.objects.create(email=email, messaggio=messaggio)

        messages.success(request, "Grazie per averci contattato! Ti risponderemo presto.")
        return redirect("contattaci")  # ricarica la pagina mostrando il messaggio
    return render(request, 'rolls/contattaci.html')

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')

def _get_cart(session):
    cart = session.get('cart', {})
    session['cart'] = cart
    return cart

def _cart_items(cart):
    items = []
    #converti la lista in dizionario
    for rid, qty in cart.items():
        try:
            rid_int = int(rid)
        except:
            continue
        roll = Roll.objects.filter(pk=rid_int).first()
        if not roll:
            continue
        items.append({'roll': roll, 'quantita': qty, 'prezzo_unitario': roll.prezzo, 'subtotal': roll.prezzo * qty})
    return items

#Controlla che il prodotto esista nel database prima di aggiungerlo al carrello
@login_required(login_url='/rolls/accounts/login/')
def aggiungi_al_carrello(request, roll_id):
    roll = get_object_or_404(Roll, pk=roll_id)
    cart = _get_cart(request.session)
    rid = str(roll.id)
    cart[rid] = cart.get(rid, 0) + 1
    request.session.modified = True
    return redirect('carrello')

@login_required(login_url='/rolls/accounts/login/')
def aggiorna_carrello(request, roll_id, action):
    cart = _get_cart(request.session)
    rid = str(roll_id)
    if action == "add":
        cart[rid] = cart.get(rid, 0) + 1
    elif action == "remove":
        if rid in cart:
            cart[rid] -= 1
            if cart[rid] <= 0:
                cart.pop(rid, None)
    elif action == "delete":
        cart.pop(rid, None)
    request.session.modified = True
    return redirect('carrello')

def carrello(request):
    cart = request.session.get("cart", {})
    if isinstance(cart, list):
        cart = {str(roll_id): 1 for roll_id in cart}

    request.session["cart"] = cart  # aggiorno la sessione
    # Ora possiamo processare i prodotti normalmente
    items = _cart_items(cart)
    totale = sum(i['subtotal'] for i in items)

    return render(request, "rolls/carrello.html", {"items": items, "totale": totale})


class CheckoutForm(forms.Form):
    indirizzo_spedizione = forms.CharField(max_length=255, label="Indirizzo di spedizione")
    metodo_pagamento = forms.ChoiceField(choices=[
        ("visa", "Visa"),
        ("mastercard", "Mastercard"),
        ("paypal", "PayPal"),
        ("klarna", "Klarna"),
    ], label="Metodo di pagamento")

@login_required(login_url='/rolls/accounts/login/')
def checkout(request):
    cart = _get_cart(request.session)
    items = _cart_items(cart)
    if not items:
        return redirect('carrello')
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            ordine = Ordine.objects.create(
                cliente=request.user,
                indirizzo_spedizione=form.cleaned_data['indirizzo_spedizione'],
                metodo_pagamento=form.cleaned_data['metodo_pagamento'],
            )
            for it in items:
                OrdineItem.objects.create(
                    ordine=ordine,
                    roll=it['roll'],
                    prezzo_unitario=it['prezzo_unitario'],
                    quantita=it['quantita'],
                )
            request.session['cart'] = {}
            request.session.modified = True
            return render(request, 'rolls/ordine_confermato.html', {'ordine': ordine})
    else:
        form = CheckoutForm()
    totale = sum(i['subtotal'] for i in items)
    return render(request, 'rolls/checkout.html', {'form': form, 'items': items, 'totale': totale})

def signup(request):
    from .forms import SignUpForm
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
