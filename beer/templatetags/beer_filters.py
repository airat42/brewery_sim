from django import template

register = template.Library()

@register.filter
def srm_to_hex(value):
    """Превращает SRM в HEX-код для цвета"""
    try:
        srm = float(value)
    except:
        srm = 0

    # простая формула преобразования SRM → RGB
    r = max(0, min(255, int(255 - srm*1.5)))
    g = max(0, min(255, int(255 - srm*0.7)))
    b = max(0, min(255, int(255 - srm*0.2)))

    return f'rgb({r},{g},{b})'
