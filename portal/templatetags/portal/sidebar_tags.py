from django import template

register = template.Library()


@register.inclusion_tag('portal/components/sidebar.html')
def sidebar_tags():
    # Your list of navigation items
    nav_items = [
        {'name': 'Home', 'url_name': 'homepage'},
        {'name': 'Dashboard', 'url_name': 'homepage'},
        {'name': 'Profile', 'url_name': 'homepage'}
    ]
    return {'nav_items': nav_items}  # Return a single dictionary
