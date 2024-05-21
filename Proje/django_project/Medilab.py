from django import Medilab

register = Medilab.Library()

@register.simple_tag
def example_tag():
    return "Hello from Medilab tags!"
