from django.shortcuts import get_object_or_404, render, redirect
from .models import Product
from .forms import CustomPackageRequestForm


def product_list(request):
    products = Product.objects.filter(available=True)
    return render(
        request,
        'shop/product/list.html',
        {
            'products': products
        }
    )


def product_detail(request, id, slug):
    product = get_object_or_404(
        Product, id=id, slug=slug, available=True
    )
    return render(
        request,
        'shop/product/detail.html',
        {'product': product}
    )


def custom_package_request(request):
    if request.method == 'POST':
        form = CustomPackageRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop:custom_request_thanks')
    else:
        form = CustomPackageRequestForm()
    return render(request, 'shop/custom_request_form.html', {'form': form})


def custom_request_thanks(request):
    return render(request, 'shop/custom_request_thanks.html')
