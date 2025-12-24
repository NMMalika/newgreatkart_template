from .models import Category

def menu_links(request):
    """A context processor to add category links to the context."""
    links = Category.objects.all()
    return dict(links=links)