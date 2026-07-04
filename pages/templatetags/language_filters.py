from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def lang_field(context, obj, field_prefix):
    """
    Достаёт поле объекта с суффиксом _ua или _en в зависимости от текущего языка.
    Использование в шаблоне: {% lang_field event 'title' %}
    """
    lang = context.get('current_language', 'en')
    field_name = f'{field_prefix}_{lang}'
    return getattr(obj, field_name, '')