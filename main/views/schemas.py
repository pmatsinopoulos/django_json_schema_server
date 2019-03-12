import json
import jsonschema
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from lib.validate_json import validate_json_content


@require_http_methods(['POST'])
def validate(request):
    error = None

    try:
        validate_json_content(request.body)
    except jsonschema.exceptions.ValidationError as e:
        error = {
            'error': e.message
        }
    except json.decoder.JSONDecodeError as e:
        error = {
            'error': 'not valid JSON document. Specific error: {}'.format(' - '.join(e.args))
        }

    if error:
        return JsonResponse(data=error, safe=True, status=422)

    return HttpResponse(status=200)
