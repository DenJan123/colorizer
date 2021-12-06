# Create your serializers here.
from rest_framework import serializers
from . import utils


class ModifyColorSerializer(serializers.Serializer):
    representation = serializers.RegexField(regex='^rgb$|^hsv$|^hex$|^hsl$')
    operation = serializers.RegexField(regex='^desaturate$|^saturate$')
    color = serializers.ListField(min_length=3, max_length=3,
                                  child=serializers.FloatField(max_value=360, min_value=0))
    amount = serializers.FloatField(min_value=0, max_value=100)


class ConvertColorSerializer(serializers.Serializer):
    representation = serializers.RegexField(regex='^rgb$|^hsv$|^hex$|^hsl$')
    conversion = serializers.RegexField(regex='^rgb$|^hsv$|^hex$|^hsl$')

    def validate(self, data):
        if data['representation'] == data['conversion']:
            raise serializers.ValidationError("You can't convert to the same color system")
        return data


class RgbSerializer(serializers.Serializer):
    color = serializers.ListField(min_length=3, max_length=3, child=
    serializers.FloatField(max_value=255, min_value=0))

    # def validate_color(self):
    #     return all(map(lambda x: 0 <= x <= 255, self.color))


class HexSerializer(serializers.Serializer):
    color = serializers.RegexField(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')


class HslSerializer(serializers.Serializer):
    color = serializers.ListField(min_length=3, max_length=3, child=
    serializers.FloatField(max_value=360, min_value=0))

    def validate_color(self, value):
        if not all(map(lambda x: 0 <= x <= 100, value[1:])):
            raise serializers.ValidationError("Second and third color values has to be from 0 to 100")
        return value


class HsvSerializer(serializers.Serializer):
    color = serializers.ListField(min_length=3, max_length=3, child=
    serializers.FloatField(max_value=360, min_value=0))

    def validate_color(self, value):
        if not all(map(lambda x: 0 <= x <= 100, value[1:])):
            raise serializers.ValidationError("Second and third color values has to be from 0 to 100")
        return value

class ColorHarmonySerializer(serializers.Serializer):
    harmony = serializers.RegexField(regex='^monochromatic$')
    color = serializers.ListField(min_length=3, max_length=3,
                                  child=serializers.FloatField(max_value=360, min_value=0))
    representation = serializers.RegexField(regex='^hsv$')

    def validate_color(self, value):
        if not all(map(lambda x: 0 <= x <= 100, value[1:])):
            raise serializers.ValidationError("Second and third color values has to be from 0 to 100")
        return value
