from .models import SubCategory
from .models import SuperCategory


def products_context_processor(request):
    context = {'categories': SubCategory.objects.all(),
               'supercategories': SuperCategory.objects.all(),
               'search_keyword': '',
               'all': ''
               }

    if 'search_keyword' in request.GET:
        keyword = request.GET['search_keyword']
        if keyword:
            context['search_keyword'] = '?keyword=' + keyword
            context['all'] = context['search_keyword']
        if 'page' in request.GET:
            page = request.GET['page']
            if page != '1':
                context['all'] += '&page=' + page
            else:
                context['all'] = '?page=' + page
    return context
