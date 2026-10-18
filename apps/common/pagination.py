from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination with clean meta envelope.
    Supports both `per_page` and `perPage` query params.
    """

    page_query_param = 'page'
    page_size_query_param = 'per_page'
    page_size = 20
    max_page_size = 50

    def get_page_size(self, request):
        if 'perPage' in request.query_params:
            try:
                size = int(request.query_params['perPage'])
                if size > 0:
                    return min(size, self.max_page_size)
            except (ValueError, TypeError):
                pass
        return super().get_page_size(request)

    def get_paginated_response(self, data):
        return Response({
            'data': data,
            'meta': {
                'total': self.page.paginator.count,
                'last_page': self.page.paginator.num_pages,
                'current_page': self.page.number,
                'per_page': self.get_page_size(self.request),
                'prev': self.page.previous_page_number() if self.page.has_previous() else None,
                'next': self.page.next_page_number() if self.page.has_next() else None,
            }
        })
