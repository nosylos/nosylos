from djangorestframework_camel_case.settings import api_settings
from djangorestframework_camel_case.util import camelize
from rest_framework.renderers import JSONRenderer


class CamelCaseJsonRenderer(JSONRenderer):
    format = "json_camel_case"
    json_underscoreize = api_settings.JSON_UNDERSCOREIZE

    def render(self, data, *args, **kwargs):
        return super().render(
            camelize(data, **self.json_underscoreize), *args, **kwargs
        )


class SnakeCaseJsonRenderer(JSONRenderer):
    format = "json_snake_case"
