"""
Advanced Pagination Classes for API

This module provides custom pagination classes with enhanced features
including configurable page sizes, metadata, and response formatting.
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination class with configurable page size.
    
    Features:
    - Configurable page size via query parameter
    - Maximum page size limit
    - Comprehensive pagination metadata
    - Custom response format
    
    Query Parameters:
        page (int): Page number (default: 1)
        page_size (int): Number of items per page (default: 20, max: 100)
    
    Response Format:
        {
            "count": total_items,
            "next": next_page_url,
            "previous": previous_page_url,
            "page_size": current_page_size,
            "total_pages": total_pages,
            "current_page": current_page,
            "results": [...]
        }
    """
    
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        """Return paginated response with additional metadata."""
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page_size': self.get_page_size(self.request),
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })


class LargeResultsSetPagination(PageNumberPagination):
    """
    Large pagination class for bulk data operations.
    
    Features:
    - Larger default page size for bulk operations
    - Higher maximum page size limit
    - Optimized for data export scenarios
    
    Query Parameters:
        page (int): Page number (default: 1)
        page_size (int): Number of items per page (default: 50, max: 500)
    """
    
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 500
    
    def get_paginated_response(self, data):
        """Return paginated response with metadata."""
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page_size': self.get_page_size(self.request),
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })


class SmallResultsSetPagination(PageNumberPagination):
    """
    Small pagination class for summary views.
    
    Features:
    - Small page size for quick previews
    - Lower maximum page size limit
    - Optimized for mobile and summary views
    
    Query Parameters:
        page (int): Page number (default: 1)
        page_size (int): Number of items per page (default: 5, max: 20)
    """
    
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20
    
    def get_paginated_response(self, data):
        """Return paginated response with metadata."""
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page_size': self.get_page_size(self.request),
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })
