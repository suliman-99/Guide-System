from rest_framework import parsers
from .funcs import deep_snake_case_transform


class SnakeCaseParser(parsers.JSONParser):

    def parse(self, stream, media_type=None, parser_context=None):
        stream = super().parse(stream, media_type, parser_context)
        return deep_snake_case_transform(stream)