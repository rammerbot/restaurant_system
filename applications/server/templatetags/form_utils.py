from django import template

register = template.Library()

@register.filter(name='get_dish_field')
def get_dish_field(form, args):
    dish_id, field_type = args.split(',')
    field_name = f'dish_{dish_id}_{field_type}'
    try:
        return form[field_name]
    except KeyError:
        return None