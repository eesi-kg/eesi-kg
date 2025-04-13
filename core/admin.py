from django.contrib import admin
from django.apps import apps
from django.db import models

# Get all models
all_models = apps.get_models()

# Define the desired order of apps
APP_ORDER = [
    'real_estate_advertisement',
    'vehicle_advertisement',
    'user',
    'common',
    'real_estate',
    'vehicle',
]

# Register all models with admin.site
for model in all_models:
    try:
        # Create a basic admin class
        admin_class = type(f'{model.__name__}Admin', (admin.ModelAdmin,), {
            'list_display': [field.name for field in model._meta.fields if field.name != 'id'],
            'search_fields': [field.name for field in model._meta.fields if isinstance(field, (models.CharField, models.TextField))],
        })
        
        # Register the model with admin.site
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        # Skip if model is already registered
        continue
