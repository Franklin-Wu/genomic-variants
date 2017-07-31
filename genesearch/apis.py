from django.http import JsonResponse

from .models import Genes

# Create your apis here.

class JsonResponseNoSuchRequest(JsonResponse):
    def __init__(self, request):
        super(JsonResponseNoSuchRequest, self).__init__(
            dict(
                error = dict(
                    code = 404, # Not Found
                    message = 'no such request ' + request
                )
            )
        )

class JsonResponseNoSuchMethod(JsonResponse):
    def __init__(self, request, method):
        super(JsonResponseNoSuchMethod, self).__init__(
            dict(
                error = dict(
                    code = 404, # Not Found
                    message = request + ' has no such method ' + method
                )
            )
        )

class JsonResponseMethodRequiresParameter(JsonResponse):
    def __init__(self, request, method, parameter):
        super(JsonResponseMethodRequiresParameter, self).__init__(
            dict(
                error = dict(
                    code = 400, # Bad Request
                    message = request + ' ' + method + ' requires parameter ' + parameter
                )
            )
        )

class JsonResponseMethodParameterTooShort(JsonResponse):
    def __init__(self, request, method, parameter, min_char_count):
        super(JsonResponseMethodParameterTooShort, self).__init__(
            dict(
                error = dict(
                    code = 400, # Bad Request
                    message = request + ' ' + method + ' parameter ' + parameter + ' requires at least ' + str(min_char_count) + ' characters'
                )
            )
        )

def noSuchRequest(request):
    return JsonResponseNoSuchRequest(request.path)

def getGeneNamesStartingWith(request):
    response = None
    key = 'prefix'
    # The min_char_count is 1 to prevent retrieving everything. Note that this need not be the same as the autocomplete element
    # minLength in a client HTML app. In fact, in the HTML app which demonstrates the use of this API sets minLength to 2. The
    # only requirement is that the client HTML app's autocomplete minLength be >= min_char_count.
    min_char_count = 1
    if request.method != 'GET':
        response = JsonResponseNoSuchMethod(request.path, request.method)
    else:
        params = request.GET;
        if not key in params:
            response = JsonResponseMethodRequiresParameter(request.path, request.method, key)
        else:
            prefix = params[key]
            if len(prefix) < min_char_count:
                response = JsonResponseMethodParameterTooShort(request.path, request.method, key, min_char_count)
            else:
                # The 'i' in '__istartswith' indicates a case-insensitive search.
                genes = Genes.objects.filter(name__istartswith = prefix).only('name')
                gene_set = set()
                for gene in genes:
                    gene_set.add(gene.name)
                response_data = dict(
                    data = dict(
                        names = sorted(list(gene_set))
                    )
                )
                response = JsonResponse(response_data)
    return response

def getGenesNamed(request):
    response = None
    key = 'name'
    if request.method != 'GET':
        response = JsonResponseNoSuchMethod(request.path, request.method)
    else:
        params = request.GET
        if not key in params:
            response = JsonResponseMethodRequiresParameter(request.path, request.method, key)
        else:
            genes = Genes.objects.filter(name = params[key]).only(
                'name',
                'nchange',
                'pchange',
                'alias',
                'region',
                'rclass',
                'leval',
                'lupdate',
                'url'
            ).order_by(
                'nchange',
                'pchange',
                'alias',
                'region',
                'rclass',
                'leval',
                'lupdate'
            )
            gene_list = []
            for gene in genes:
                gene_list.append(
                    dict(
                        name    = gene.name,
                        nchange = gene.nchange,
                        pchange = gene.pchange,
                        alias   = gene.alias,
                        region  = gene.region,
                        rclass  = gene.rclass,
                        leval   = gene.leval,
                        lupdate = gene.lupdate,
                        url     = gene.url
                    )
                )
            response_data = dict(
                data = gene_list
            )
            response = JsonResponse(response_data)
    return response
