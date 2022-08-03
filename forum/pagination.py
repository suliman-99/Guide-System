from rest_framework.pagination import PageNumberPagination


class PageNumberPagination10(PageNumberPagination):
    page_size = 10
