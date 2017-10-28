from django.http import HttpResponse, HttpResponseServerError

from onelogin.saml2.settings import OneLogin_Saml2_Settings
from .saml import SpidSaml2Auth

from .apps import SpidConfig


def init_saml_auth(request):
    print(request['get_data'])
    auth = SpidSaml2Auth(request, old_settings=SpidConfig.get_saml_settings(request['get_data'].get('idp')))
    # auth = OneLogin_Saml2_Auth(request, old_settings=SpidConfig.saml_settings)
    return auth


def get_request_data(request):
    # If server is behind proxys or balancers use the HTTP_X_FORWARDED fields
    result = {
        'https': 'on' if request.is_secure() else 'off',
        'http_host': request.META['HTTP_HOST'],
        'script_name': request.META['PATH_INFO'],
        'server_port': request.META['SERVER_PORT'],
        'get_data': request.GET.copy(),
        # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
        # 'lowercase_urlencoding': True,
        'post_data': request.POST.copy()
    }
    return result


def metadata(request):
    saml_settings = OneLogin_Saml2_Settings(settings=SpidConfig.get_saml_settings(), sp_validation_only=True)
    sp_metadata = saml_settings.get_sp_metadata()
    errors = saml_settings.validate_metadata(sp_metadata)

    if len(errors) == 0:
        resp = HttpResponse(content=sp_metadata, content_type='text/xml')
    else:
        resp = HttpResponseServerError(content=', '.join(errors))
    return resp
