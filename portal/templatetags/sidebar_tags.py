from django import template

register = template.Library()


# @register.inclusion_tag('portal/components/sidebar.html')
# def sidebar_tags():
#     # Your list of navigation items
#     nav_items = [
#         {'name': 'Home', 'url_name': 'homepage'},
#         {'name': 'Dashboard', 'url_name': 'homepage'},
#         {'name': 'Profile', 'url_name': 'homepage'}
#     ]
#     return {'nav_items': nav_items}  # Return a single dictionary

 
@register.inclusion_tag('portal/components/dynamic_sidebar.html', takes_context=True)
def sidebar_tags(context):
    # Get the user from the context
    request = context['request']
    user = request.user

    # Default navigation items for all authenticated users
    nav_items = [
        {'name': 'Home', 'url_name': 'homepage'}
    ]
    i = user.groups.values_list('name', flat=True)
    print(list(i))
    # Add more navigation items based on user's group membership
    if user.is_authenticated:
        # Always add Upload option for authenticated users
        nav_items.append(
            {'name': 'Author', 'url_name': 'portal:portal', 'mode': 'Author'})

        # Add Viewer option only for users in the Editor group
        if user.groups.filter(name='Editor').exists():
            nav_items.append(
                {'name': 'Editor', 'url_name': 'portal:portal', 'mode': 'Editor'})
 
        # You can add more group-specific navigation items here
        # Example: Admin group specific items
        if user.groups.filter(name='Admin').exists():
            nav_items.append(
                {'name': 'Admin Panel', 'url_name': 'admin:index'})

    # Return both navigation items and the current active tab
    return {
        'nav_items': nav_items,
        'active_tab': context.get('active_tab', 'author')
    }
