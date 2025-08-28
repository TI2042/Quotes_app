import random

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import QuoteForm
from .models import Quote


def weighted_random_quote():
    quotes = list(Quote.objects.all())
    weights = [q.weight for q in quotes]
    return random.choices(quotes, weights=weights, k=1)[0] if quotes else None


def quote_view(request):
    quote = weighted_random_quote()
    if quote:
        quote.views += 1
        quote.save()
    return render(request, "quotes/quote.html", {"quote": quote})


def add_quote(request):
    form = QuoteForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("home")
    return render(request, "quotes/add.html", {"form": form})


def vote(request, quote_id, action):
    quote = get_object_or_404(Quote, id=quote_id)
    if action == "like":
        quote.likes += 1
    elif action == "dislike":
        quote.dislikes += 1
    quote.save()
    return redirect("home")


def top_quotes(request):
    sort_by = request.GET.get("sort_by", "likes")

    if sort_by == "dislikes":
        quotes = Quote.objects.order_by("-dislikes")[:10]
    elif sort_by == "views":
        quotes = Quote.objects.order_by("-views")[:10]
    else:  # default: likes
        quotes = Quote.objects.order_by("-likes")[:10]

    return render(
        request, "quotes/top.html", {"top_quotes": quotes, "current_sort": sort_by}
    )


def all_quotes_view(request):
    query = request.GET.get("q")
    sort_by = request.GET.get("sort", "id")  # сортировка по умолчанию
    order = request.GET.get("order", "asc")

    quotes = Quote.objects.all()

    if query:
        quotes = quotes.filter(Q(text__icontains=query) | Q(source__icontains=query))

    if order == "desc":
        sort_by = f"-{sort_by}"

    quotes = quotes.order_by(sort_by)

    paginator = Paginator(quotes, 10)  # 10 цитат на страницу
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "quotes/all_quotes.html", {
        "page_obj": page_obj,
        "query": query,
        "sort": sort_by,
        "order": order
    })


def edit_quote_view(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    if request.method == "POST":
        form = QuoteForm(request.POST, instance=quote)
        if form.is_valid():
            form.save()
            return redirect("all_quotes")
    else:
        form = QuoteForm(instance=quote)
    return render(request, "quotes/edit_quote.html", {"form": form, "quote": quote})


def delete_quote_view(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    if request.method == "POST":
        quote.delete()
        return redirect("all_quotes")
    return render(request, "quotes/delete_quote.html", {"quote": quote})
