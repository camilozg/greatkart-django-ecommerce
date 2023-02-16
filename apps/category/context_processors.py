from .models import Category


def categories(request):
    return dict(categories=Category.objects.all())
