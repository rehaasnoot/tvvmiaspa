REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
#        'rest_framework_simplejwt.authentication.JSONWebTokenAuthentication',
#        'djangorestframework_simplejwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.permissions.IsAuthenticated',
        #'rest_framework.authentication.TokenAuthentication',
#        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
INSTALLED_APPS = [
    'rest_framework',
]