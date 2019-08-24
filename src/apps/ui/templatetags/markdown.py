import markdown

from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(name="markdown", is_safe=True)
def markdown_filter(value):
    return mark_safe(markdown.markdown(value))


@register.tag(name="markdown")
def markdown_tag(parser, token):
    nodelist = parser.parse(("endmarkdown",))
    parser.delete_first_token()  # consume '{% endmarkdown %}'
    return MarkdownNode(nodelist)


class MarkdownNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        value = self.nodelist.render(context)
        return mark_safe(markdown.markdown(value))
