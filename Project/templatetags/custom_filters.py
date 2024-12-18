from django import template

register = template.Library()

@register.filter(name='contain_string')
def contain_string(text1, text2):
    return text2 in text1
@register.filter(name='admin_show_comparison_state')
def admin_show_comparison_state(text):
    return text == "已开始"