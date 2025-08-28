import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quote
from .forms import QuoteForm
def weighted_random_quote():
    quotes = list(Quote.objects.all())
    weights = [q.weight for q in quotes]
    return random.choices(quotes, weights=weights, k=1)[0] if quotes else None
def quote_view(request):
    quote = weighted_random_quote()
    if quote:
        quote.views += 1
        quote.save()
    return render(request, 'quotes/quote.html', {'quote': quote})
def add_quote(request):
    form = QuoteForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('random_quote')
    return render(request, 'quotes/add.html', {'form': form})
def vote(request, quote_id, action):
    quote = get_object_or_404(Quote, id=quote_id)
    if action == 'like':
        quote.likes += 1
    elif action == 'dislike':
        quote.dislikes += 1
    quote.save()
    return redirect('random_quote')
def top_quotes(request):
    quotes = Quote.objects.order_by('-likes')[:10]
    return render(request, 'quotes/top.html', {'top_quotes': quotes})
