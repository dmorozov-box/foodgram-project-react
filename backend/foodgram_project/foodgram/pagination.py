from rest_framework.pagination import PageNumberPagination


class PageNumberAndLimitPagination(PageNumberPagination):
    page_size_query_param = 'limit'
