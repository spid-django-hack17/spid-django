from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from onelogin.saml2.utils import OneLogin_Saml2_Utils
from spid.views import get_request_data, init_saml_auth


def index(request):
    request_data = get_request_data(request)
    auth = init_saml_auth(request_data)
    print("AUTH: ", auth)
    #import pdb
    #pdb.set_trace()
    errors = []
    not_auth_warn = False
    success_slo = False
    attributes = False
    paint_logout = False

    if 'sso' in request.GET:
        return HttpResponseRedirect(auth.login())

    elif 'sso2' in request.GET:
        return_to = OneLogin_Saml2_Utils.get_self_url(request_data) + reverse('demo:attrs')
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
        template_name='index.html',
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

    return render(request, 'attrs.html', {'paint_logout': paint_logout, 'attributes': attributes})
