# init.py: Updated to ensure Django uses the custom BlogConfig for app configuration by adding
# default_app_config = 'blog.apps.BlogConfig', which is crucial for activating the
# signals setup in apps.py and signals.py.

default_app_config = 'blog.apps.BlogConfig'
