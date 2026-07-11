from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def lang_field(context, obj, field_prefix):
    """
    Достаёт поле объекта с суффиксом _ua или _en в зависимости от текущего языка.
    Если запрошено _en, но поле пустое — падает обратно на _ua (лучше показать
    украинский текст, чем пустое место).
    Использование в шаблоне: {% lang_field event 'title' %}
    """
    lang = context.get('current_language', 'en')
    field_name = f'{field_prefix}_{lang}'
    value = getattr(obj, field_name, '')

    if not value and lang == 'en':
        value = getattr(obj, f'{field_prefix}_ua', '')

    return value