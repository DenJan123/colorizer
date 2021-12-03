from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import Color


# do the calculation and return the dict object to convert into json object in post response


@api_view(["GET", "POST"])
def modify_color(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == "GET":
        return Response('')

    elif request.method == "POST":
        query = Color(**request.data)
        is_done = query.perform_operation()

        if is_done:
            return Response(query.return_data())
        else:
            return Response({'error': 'Invalid data.'}, status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def convert_color(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == "GET":
        return Response('')

    elif request.method == "POST":
        query = Color(**request.data)
        result = query.convert_color()
        if result:
            return Response(result)
        else:
            return Response({'error': 'Invalid data.'}, status.HTTP_400_BAD_REQUEST)
