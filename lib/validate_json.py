import json

import jsonschema
import urllib.request

from django.conf import settings

FILE_PROTOCOL = 'file://'


def validate_json_content(json_content):
    json_content = json.loads(json_content)
    schema = json_content['$schema']

    if schema.startswith(FILE_PROTOCOL):
        schema_json_file_name = schema[len(FILE_PROTOCOL) + 1:]
        schema_json_file_name = "{}/{}".format(settings.SCHEMAS_LOCAL_DIR, schema_json_file_name)

        schema_content = open(schema_json_file_name).read()
        schema_content = json.loads(schema_content)
    else:
        schema_content = urllib.request.urlopen(schema).read()
        schema_content = json.loads(schema_content)

    jsonschema.validate(json_content, schema_content)

    return True
