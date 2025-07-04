from django.shortcuts import render


def about(request):
    context = {
        'hero_image': 'images/azwedo-l-lc-nbEX3qxtmuA-unsplash.jpg',
        'hero_image_is_static': True,
        'show_hero_text': False,
        'hero_title': 'About Our Web Development Services',
        'hero_subtitle': 'Professional, modern, and affordable solutions',
    }
    return render(request, 'pages/about.html', context)
