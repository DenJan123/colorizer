from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import Color
from .serializers import RgbSerializer, HexSerializer, HslSerializer, ConvertColorSerializer, HsvSerializer, \
    ModifyColorSerializer, ColorHarmonySerializer


# do the calculation and return the dict object to convert into json object in post response


@api_view(["GET", "POST"])
def modify_color(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == "GET":
        return Response('')

    elif request.method == "POST":
        req = ModifyColorSerializer(data=request.data)
        if not req.is_valid():
            return Response({'error': 'Invalid data.'}, status.HTTP_400_BAD_REQUEST)
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

        # conv_ser = ConvertColorSerializer(data={
        #     'representation' : request.data['representation'],
        #     'conversion' : request.data['conversion']
        # })

        conv_serializer = ConvertColorSerializer(data=request.data)  # seems to be valid aswell

        if request.data['representation'] == 'rgb':
            color_serializer = RgbSerializer(data=request.data)
        elif request.data['representation'] == 'hex':
            color_serializer = HexSerializer(data=request.data)
        elif request.data['representation'] == 'hsl':
            color_serializer = HslSerializer(data=request.data)
        elif request.data['representation'] == 'hsv':
            color_serializer = HsvSerializer(data=request.data)
        else:
            color_serializer = False

        if (not conv_serializer.is_valid()
                or not color_serializer
                or not color_serializer.is_valid()):
            return Response({'error': 'Invalid data.'}, status.HTTP_400_BAD_REQUEST)

        query = Color(**request.data)
        result = query.convert_color()

        if result:
            return Response(result)
        else:
            return Response({'error': 'Invalid data.'}, status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def color_harmony(request, format=None):
    color_harmony_inst = ColorHarmonySerializer(data=request.data)
    if color_harmony_inst.is_valid():
        query = Color(**request.data)
        harmony_color_dict = query.make_harmony_colors()
        return Response({"representation": "hsv",
                        **harmony_color_dict})
    else:
        return Response({'error': 'Invalid data.'}, status.HTTP_400_BAD_REQUEST)
