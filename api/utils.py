import colorsys
import bisect

ADOBE_ARTIST_WHEEL = {
    0: 0,  # red
    35: 60,  # orange
    60: 122,  # yellow
    120: 165,  # green
    180: 218,  # cyan
    240: 275,  # blue
    300: 330,  # magenta
    360: 360  # red
}
ADOBE_ARTIST_WHEEL_REVERSE = {v: k for k, v in ADOBE_ARTIST_WHEEL.items()}


def get_adobe_artist_wheel_hue_range(hue, dict_with_values=ADOBE_ARTIST_WHEEL):
    keys = list(dict_with_values.keys())
    index = bisect.bisect_right(keys, hue) - 1
    return (keys[index], keys[(index + 1) % len(keys)])


def get_adobe_artist_wheel_artist_range(hue, dict_with_values=ADOBE_ARTIST_WHEEL):
    a, b = get_adobe_artist_wheel_hue_range(hue, dict_with_values=dict_with_values)
    return (dict_with_values[a], dict_with_values[b])


# def get_adobe_artist_wheel_artist_range(hue):
#     values = list(ADOBE_ARTIST_WHEEL.values())
#     index = bisect.bisect_right(values, hue) - 1
#     return (values[index], values[index + 1])


def convert_hsv_hue_to_artistic_hue(hue, dict_with_values=ADOBE_ARTIST_WHEEL):
    h_range = get_adobe_artist_wheel_hue_range(hue, dict_with_values=dict_with_values)
    a_range = get_adobe_artist_wheel_artist_range(hue, dict_with_values=dict_with_values)
    return (hue - h_range[0]) / (h_range[1] - h_range[0]) * (a_range[1] - a_range[0]) + a_range[0]


def find_complementary(hue):
    artistic = convert_hsv_hue_to_artistic_hue(hue, dict_with_values=ADOBE_ARTIST_WHEEL)
    comp_artistic = (artistic + 180) % 360
    hsv_color = convert_hsv_hue_to_artistic_hue(comp_artistic, dict_with_values=ADOBE_ARTIST_WHEEL_REVERSE)
    return round(hsv_color)



print('here')


class Color:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        # self.check_validations()

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
            # if not self.valid_for_desaturate_saturate():
            #     return False
            value = int(round(self.color[1] - self.color[1] * self.amount / 100))
            if value > 100:
                value = 100
            if value < 0:
                value = 0
            self.modified_color = self.color[:]
            self.modified_color[1] = value
            return True
        elif self.operation == 'saturate':
            # if not self.valid_for_desaturate_saturate():
            #     return False
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
        # if not self.valid_for_conversion_color():
        #     return False
        if self.representation == 'rgb':
            if self.conversion in ('hsv', 'hsl'):
                red, green, blue = self.color

                # get rgb percentage: range (0-1, 0-1, 0-1 )
                red_percentage = red / float(255)
                green_percentage = green / float(255)
                blue_percentage = blue / float(255)

                # get hsv percentage: range (0-1, 0-1, 0-1)
                if self.conversion == 'hsv':
                    color_hsv_percentage = colorsys.rgb_to_hsv(red_percentage, green_percentage, blue_percentage)
                else:
                    color_hsv_percentage = colorsys.rgb_to_hls(red_percentage, green_percentage, blue_percentage)
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
            elif self.conversion == 'hex':
                converted_color = "#{:02x}{:02x}{:02x}".format(*self.color).upper()
                return {
                    'color': self.color,
                    'converted_color': converted_color
                }
        elif (self.representation == 'hsv' and self.conversion == 'hsl') \
                or (self.representation == 'hsl' and self.conversion == 'hsv'):
            data = {
                'representation': self.representation,
                'color': self.color,
                'conversion': 'rgb'
            }
            rgb_result = Color(**data).convert_color()['converted_color']
            data = {
                'representation': 'rgb',
                'color': rgb_result,
                'conversion': self.conversion
            }
            res_color = Color(**data).convert_color()
            return res_color


        elif self.representation in ['hsv', 'hsl']:
            if self.conversion == 'rgb':
                h = self.color[0] / float(360)
                s = self.color[1] / float(100)
                v = self.color[2] / float(100)

                if self.representation == 'hsv':
                    color_rgb_percentage = colorsys.hsv_to_rgb(h, s, v)
                else:
                    color_rgb_percentage = colorsys.hls_to_rgb(h, v, s)
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
            elif self.conversion == 'hex':
                data = {
                    'representation': self.representation,
                    'color': self.color,
                    'conversion': 'rgb'
                }
                rgb_result = Color(**data).convert_color()['converted_color']
                data = {
                    'representation': 'rgb',
                    'color': rgb_result,
                    'conversion': 'hex'
                }
                hex_color = Color(**data).convert_color()
                return hex_color


        elif self.representation == 'hex':
            if self.conversion == 'rgb':
                return {
                    'color': self.color,
                    'converted_color': list(int(self.color[1:][i:i + 2], 16) for i in (0, 2, 4))
                }
            if self.conversion in ['hsv', 'hsl']:
                data = {
                    'representation': self.representation,
                    'color': self.color,
                    'conversion': 'rgb'
                }
                rgb_result = Color(**data).convert_color()['converted_color']
                data = {
                    'representation': 'rgb',
                    'color': rgb_result,
                    'conversion': self.conversion
                }
                res_color = Color(**data).convert_color()
                return res_color

    def make_harmony_colors(self):
        h, s, v = self.color[:]
        v_shade, v_tint = 0, 0
        if 20 <= v <= 80:
            v_shade = v - 20
            if v_shade < 0:
                v_shade = 0
            v_tint = v + 20
            if v_shade > 100:
                v_tint = 100
        elif v - 20 < 0:
            v_shade = v + 20
            v_tint = v + 40
        elif v + 20 > 100:
            v_shade = v - 20
            v_tint = v - 40
        base_color = [h, s, v]
        shade_color = [h, s, v_shade]
        tint_color = [h, s, v_tint]
        res_list = sorted([base_color, shade_color, tint_color], key=lambda color: color[2])
        return {'color_1': res_list[0],
                'color_2': res_list[1],
                'color_3': res_list[2]}

    def find_complementary_color_hue(self):
        h = self.color[0]
        complementary = find_complementary(h)
        return {'complementary': [
            complementary,
            *self.color[1:]
        ]}


def validate_color(color):
    if color.representation == 'hsv':
        return (0 <= color.color[0] <= 360
                and 0 <= color.color[1] <= 100
                and 0 <= color.color[2] <= 100)
    if color.representation == 'rgb':
        return all(map(lambda x: 0 <= x <= 255, color.color))


if __name__ == "__main__":
    find_complementary(128)
