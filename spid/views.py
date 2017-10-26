from django.core.urlresolvers import reverse
from django.http import (HttpResponse, HttpResponseRedirect,
                         HttpResponseServerError)
from django.shortcuts import render

from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils
from .saml import SpidSaml2Auth
from onelogin.saml2.auth import OneLogin_Saml2_Auth

from .apps import SpidConfig


def init_saml_auth(request):
    auth = SpidSaml2Auth(request, old_settings=SpidConfig.saml_settings)
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


def index(request):
    request_data = get_request_data(request)
    auth = init_saml_auth(request_data)
    print("AUTH: ", auth)
    import pdb
    pdb.set_trace()
    errors = []
    not_auth_warn = False
    success_slo = False
    attributes = False
    paint_logout = False

    if 'sso' in request.GET:
        return HttpResponseRedirect(auth.login())

    elif 'sso2' in request.GET:
        return_to = OneLogin_Saml2_Utils.get_self_url(request_data) + reverse('spid:attrs')
        return HttpResponseRedirect(auth.login(return_to))

    elif 'slo' in request.GET:
        name_id = None
        session_index = None
        if 'samlNameId' in request.session:
            name_id = request.session['samlNameId']
        if 'samlSessionIndex' in request.session:
            session_index = request.session['samlSessionIndex']
        return HttpResponseRedirect(auth.logout(name_id=name_id, session_index=session_index))

    elif 'acs' in request.GET:
        auth.process_response()
        errors = auth.get_errors()
        not_auth_warn = not auth.is_authenticated()
        if not errors:
            request.session['samlUserdata'] = auth.get_attributes()
            request.session['samlNameId'] = auth.get_nameid()
            request.session['samlSessionIndex'] = auth.get_session_index()
            if 'RelayState' in request.POST and \
                            OneLogin_Saml2_Utils.get_self_url(request_data) != request.POST['RelayState']:
                return HttpResponseRedirect(auth.redirect_to(request.POST['RelayState']))

    elif 'sls' in request.GET:
        url = auth.process_slo(delete_session_cb=lambda: request.session.flush())
        errors = auth.get_errors()
        if len(errors) == 0:
            if url is not None:
                return HttpResponseRedirect(url)
            else:
                success_slo = True

    if 'samlUserdata' in request.session:
        paint_logout = True
        if len(request.session['samlUserdata']) > 0:
            attributes = request.session['samlUserdata'].items()

    return render(
        request=request,
        template_name='spid/index.html',
        context={
            'errors': errors,
            'not_auth_warn': not_auth_warn,
            'success_slo': success_slo,
            'attributes': attributes,
            'paint_logout': paint_logout
        })


def attrs(request):
    paint_logout = False
    attributes = False

    if 'samlUserdata' in request.session:
        paint_logout = True
        if len(request.session['samlUserdata']) > 0:
            attributes = request.session['samlUserdata'].items()

    return render(request, 'spid/attrs.html', {'paint_logout': paint_logout, 'attributes': attributes})


def metadata(request):
    saml_settings = OneLogin_Saml2_Settings(settings=SpidConfig.saml_settings, sp_validation_only=True)
    metadata = saml_settings.get_sp_metadata()
    errors = saml_settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = HttpResponse(content=metadata, content_type='text/xml')
    else:
        resp = HttpResponseServerError(content=', '.join(errors))
    return resp
