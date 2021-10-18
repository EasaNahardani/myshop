from django.shortcuts import render, get_object_or_404
from django.urls import translate_url
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _, activate, check_for_language, get_language_from_path
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Category, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender


def redirect_translated_url(request, language_code=None):
    referer = request.META.get('HTTP_REFERER')
    if not url_has_allowed_host_and_scheme(url=referer, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
            next = '/'
    else:
        lang_referer=get_language_from_path(referer)
        activate(lang_referer)
        next = translate_url(referer, language_code)
    #else:
        #activate(settings.LANGUAGE_CODE)
        #next = translate_url(referer, lang_code)
    return HttpResponseRedirect(next)


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category, translations__language_code=language, translations__slug=category_slug)
        # category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product,
                                id=id,
                                translations__language_code=language,
                                translations__slug=slug,
                                available=True)
    # product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                  'cart_product_form': cart_product_form,
                  'recommended_products': recommended_products})
