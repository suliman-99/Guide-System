from rest_framework import renderers
from .funcs import deep_camel_case_transform 

class CamelCaseRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        camelized_data = deep_camel_case_transform(data)
        return super().render(camelized_data, accepted_media_type, renderer_context)

class BrowsableCamelCaseRenderer(renderers.BrowsableAPIRenderer):
    def get_default_renderer(self, view):
        return CamelCaseRenderer()