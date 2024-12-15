from django.shortcuts import render, get_object_or_404
from antiques.models import Antique
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Category

def category(request, cat_slug=None):
    cat_name = "All Antiques"
    if cat_slug:
        cat = get_object_or_404(Category, slug=cat_slug)
        all_antique = Antique.objects.filter(category=cat).order_by('-modified_on')
        cat_name = cat.category_name
    else:
        all_antique = Antique.objects.all().order_by('-modified_on')


    paginator = Paginator(all_antique, 20)
    page = request.GET.get('page')

    try:
        antiques = paginator.page(page)
    except PageNotAnInteger:
        antiques = paginator.page(1)
    except EmptyPage:
        antiques = paginator.page(paginator.num_pages)

    context = {
        'antiques': antiques,
        'category_name': cat_name,
    }

    return render(request, 'category/antique-cat.html', context)


