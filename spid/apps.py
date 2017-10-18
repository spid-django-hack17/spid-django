from django.conf import settings
from django.apps import AppConfig


SPID_SAML_SETTINGS = {
    "strict": True,
    "debug": True,
    "sp": {
        "entityId": "https://%s/metadata/" % settings.SPID_SP_DOMAIN,
        "assertionConsumerService": {
            "url": "https://%s/?acs" % settings.SPID_SP_DOMAIN,
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
        },
        "singleLogoutService": {
            "url": "https://%s/?sls" % settings.SPID_SP_DOMAIN,
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "NameIDFormat": "urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified",
        "x509cert": open(settings.SPID_SP_PUBLIC_CERT).read(),
        "privateKey": settings.SPID_SP_PRIVATE_KEY
    },
    "idp": {
        "entityId": "https://app.onelogin.com/saml/metadata/<onelogin_connector_id>",
        "singleSignOnService": {
            "url": "https://app.onelogin.com/trust/saml2/http-post/sso/<onelogin_connector_id>",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "singleLogoutService": {
            "url": "https://app.onelogin.com/trust/saml2/http-redirect/slo/<onelogin_connector_id>",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "x509cert": "<onelogin_connector_cert>"
    }
}


class SpidConfig(AppConfig):
    name = 'spid'
    verbose_name = "SPID Authentication"

    saml_settings = dict(SPID_SAML_SETTINGS)
