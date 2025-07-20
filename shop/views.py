from django.shortcuts import get_object_or_404, render, redirect
from .models import Product
from .forms import CustomPackageRequestForm


def product_list(request):
    """Display a list of available products."""
    products = Product.objects.filter(available=True)
    return render(
        request,
        'shop/product/list.html',
        {
            'products': products,
            'hero_image': 'images/rishi--fiCYNV51m4-unsplash.jpg',
            'hero_image_is_static': True,
            'show_hero_text': True,
        }
    )


def product_detail(request, id, slug):
    """Display detailed view of a specific product."""
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    hero_image = product.image.url if product.image else None

    context = {
        'product': product,
        'hero_image': hero_image,
        'hero_image_is_static': False,
        'show_hero_text': False,
    }

    return render(request, 'shop/product/detail.html', context)


def custom_package_request(request):
    """Handle custom package request form submission."""
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
            'hero_image': 'images/diego-ph-fIq0tET6llw-unsplash.jpg',
            'hero_image_is_static': True,
            'hero_title': 'Custom Website Request',
            'hero_subtitle': "Let's build a website for your needs.",
            'show_hero_text': False,
        }
    )


def custom_request_thanks(request):
    """Display thank you page after custom request submission."""
    return render(
        request,
        'shop/custom_request_thanks.html',
        {
            'hero_image': 'images/markus-spiske-MbG7kwWptII-unsplash.jpg',
            'hero_image_is_static': True,
            'show_hero_text': False,
        }
    )
