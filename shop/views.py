from django.shortcuts import get_object_or_404, render, redirect
from .models import Product
from .forms import CustomPackageRequestForm


def product_list(request):
    products = Product.objects.filter(available=True)
    return render(
        request,
        'shop/product/list.html',
        {
            'products': products,
            'hero_image': 'images/sigmund-Im_cQ6hQo10-unsplash.jpg',
            'hero_image_is_static': True,  # This is a static file
            'hero_title': "Welcome to My Shop",
            'hero_subtitle': "Your tagline or call to action",
            'show_hero_text': True,
        }
    )


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    hero_image = product.image.url if product.image else None

    context = {
        'product': product,
        'hero_image': hero_image,  # This is a media file URL
        'hero_image_is_static': False,  # This is NOT a static file
        'hero_title': product.name,
        'hero_subtitle': getattr(product, 'short_description', '') or product.description[:100],
        'show_hero_text': True,
    }

    return render(request, 'shop/product/detail.html', context)


def custom_package_request(request):
    if request.method == 'POST':
        form = CustomPackageRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop:custom_request_thanks')
    else:
        form = CustomPackageRequestForm()
    return render(
        request,
        'shop/custom_request_form.html',
        {
            'form': form,
            'hero_image': 'images/becomes-co-7oBmQz4bfrQ-unsplash.jpg',
            'hero_image_is_static': True,  # This is a static file
            'hero_title': 'Custom Website Request',
            'hero_subtitle': "Let's build a website for your needs.",
            'show_hero_text': True,
        }
    )


def custom_request_thanks(request):
    return render(
        request,
        'shop/custom_request_thanks.html',
        {
            'hero_image': 'images/markus-spiske-MbG7kwWptII-unsplash.jpg',
            'hero_image_is_static': True,  # This is a static file
            'show_hero_text': False,
        }
    )