from django.shortcuts import render,get_object_or_404
from antiques.models import Antique
from .models import Category
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from category.models import Category



def category(request, cat_slug=None):
    cat_name = ""
    if cat_slug is None:
        all_antique = Paginator(Antique.objects.all().order_by('-modified_on'),20)
    else:
        print(cat_slug)
        cat = Category.objects.get(slug=cat_slug)
        all_antique = Paginator(Antique.objects.all().filter(category=cat).order_by('-modified_on'),20)
        cat_name= cat.category_name

    page = request.GET.get('page')

    try:
        books = all_antique.page(page)
    except PageNotAnInteger:
        books = all_antique.page(1)
    except EmptyPage:
        books = all_antique.page(1)

    context = {
        'books': books,
         'category_name':cat_name,
    }
    return render(request, 'cart/books-cat.html', context)


