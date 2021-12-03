import colorsys


class Color:
    # def __init__(self, representation, color, operation, amount):
    #     self.representation = representation
    #     self.color = color
    #     self.operation = operation
    #     self.amount = amount
    #     self.modified_color = []
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.check_validations()

    def check_validations(self):
        self.valid_fields_for_sat_desat = all(map(lambda x: x in vars(self), ('representation',
                                                                              'color',
                                                                              'operation',
                                                                              'amount')))
        self.valid_field_colors = self.validate()
        self.valid_field_representation = getattr(self, 'representation', '') in ['hsv', 'rgb']
        self.valid_fields_for_color_conversion = all(map(lambda x: x in vars(self), ('representation',
                                                                                     'color',
                                                                                     'conversion')))
        self.valid_field_conversion = getattr(self, 'conversion', '') in ['hsv', 'rgb']

    def valid_for_desaturate_saturate(self):
        return all([self.valid_fields_for_sat_desat, self.valid_field_colors, self.valid_field_representation])

    def valid_for_conversion_color(self):
        return all([self.valid_field_colors, self.valid_fields_for_color_conversion, self.valid_field_conversion,
                   self.valid_field_representation])

    def perform_operation(self):
        if self.operation == 'desaturate':
            if not self.valid_for_desaturate_saturate():
                return False
            value = int(round(self.color[1] - self.color[1] * self.amount / 100))
            if value > 100:
                value = 100
            if value < 0:
                value = 0
            self.modified_color = self.color[:]
            self.modified_color[1] = value
            return True
        elif self.operation == 'saturate':
            if not self.valid_for_desaturate_saturate():
                return False
            value = int(round(self.color[1] + self.color[1] * self.amount / 100))
            if value > 100:
                value = 100
            if value < 0:
                value = 0
            self.modified_color = self.color[:]
            self.modified_color[1] = value
            return True
        else:
            return False

    def return_data(self):
        return {
            'representation': self.representation,
            'color': self.color,
            'operation': self.operation,
            'modified_color': self.modified_color
        }

    def validate(self):
        return validate_color(self)

    def convert_color(self):
        if not self.valid_for_conversion_color():
            return False
        if self.representation == 'rgb':
            red, green, blue = self.color

            # get rgb percentage: range (0-1, 0-1, 0-1 )
            red_percentage = red / float(255)
            green_percentage = green / float(255)
            blue_percentage = blue / float(255)

            # get hsv percentage: range (0-1, 0-1, 0-1)
            color_hsv_percentage = colorsys.rgb_to_hsv(red_percentage, green_percentage, blue_percentage)
            color_h = round(360 * color_hsv_percentage[0])
            color_s = round(100 * color_hsv_percentage[1])
            color_v = round(100 * color_hsv_percentage[2])

            return {
                'color': self.color,
                'converted_color': [
                    color_h,
                    color_s,
                    color_v
                ]
            }
        if self.representation == 'hsv':
            h = self.color[0] / float(360)
            s = self.color[1] / float(100)
            v = self.color[2] / float(100)

            color_rgb_percentage = colorsys.hsv_to_rgb(h, s, v)
            red = round(255 * color_rgb_percentage[0])
            green = round(255 * color_rgb_percentage[1])
            blue = round(255 * color_rgb_percentage[2])
            return {
                'color': self.color,
                'converted_color': [
                    red,
                    green,
                    blue
                ]
            }


def validate_color(color):
    if color.representation == 'hsv':
        return (0 <= color.color[0] <= 360
                and 0 <= color.color[1] <= 100
                and 0 <= color.color[2] <= 100)
    if color.representation == 'rgb':
        return all(map(lambda x: 0 <= x <= 255, color.color))
