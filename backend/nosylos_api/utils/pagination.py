from rest_framework.pagination import PageNumberPagination


def create_custom_pagination_class(
    page_query_param="page", page_size_query_param=None, max_page_size=500
):
    """
    Creates a custom pagination class based on PageNumberPagination with
    customizable query parameters.

    :param page_query_param: The query parameter for the page number.
        Default is "page".
    :param page_size_query_param: The query parameter for the page size.
        Default is None, which means the page size is fixed.
    :param max_page_size: The maximum page size allowed.
        Default is 500.
    :return: A custom pagination class.
    """
    return type(
        "CustomPageNumberPagination",
        (PageNumberPagination,),
        {
            "page_query_param": page_query_param,
            "page_size_query_param": page_size_query_param,
            "max_page_size": max_page_size,
        },
    )
