from xml.etree import ElementTree as et

from django.conf import settings
from django.apps import AppConfig

SAML_METADATA_NAMESPACE = "urn:oasis:names:tc:SAML:2.0:metadata"
XML_SIGNATURE_NAMESPACE = "http://www.w3.org/2000/09/xmldsig#"

SPID_NAME_FORMAT = "urn:oasis:names:tc:SAML:2.0:attrname-format:basic"
SAML_BINDING_REDIRECT_URN = "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"


SPID_IDENTITY_PROVIDERS = [
    ('arubaid', 'Aruba ID'),
    ('infocertid', 'Infocert ID'),
    ('namirialid', 'Namirial ID'),
    ('posteid', 'Poste ID'),
    ('sielteid', 'Sielte ID'),
    ('spiditalia', 'SPIDItalia Register.it'),
    ('timid', 'Tim ID')
]


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
        "attributeConsumingService": {
            "serviceName": settings.SPID_SERVICE_NAME,
            "serviceDescription": settings.SPID_SERVICE_DESCRIPTION,
            "requestedAttributes": [
                {'name': name, 'nameFormat': SPID_NAME_FORMAT}
                for name in settings.SPID_REQUESTED_ATTRIBUTES
            ]
        },
        "NameIDFormat": "urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified",
        "x509cert": open(settings.SPID_SP_PUBLIC_CERT).read(),
        "privateKey": settings.SPID_SP_PRIVATE_KEY
    },
    "idp": {
        "entityId": "https://idp.spid.gov.it:9443/metadata/",
        "singleSignOnService": {
            "url": "https://idp.spid.gov.it:9443/samlsso",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "singleLogoutService": {
            "url": "https://idp.spid.gov.it:9443/samlsso",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "x509cert": (
            "MIICNTCCAZ6gAwIBAgIES343gjANBgkqhkiG9w0BAQUFADBVMQswCQYDVQQGEwJVUzELMAkGA1UE"
			"CAwCQ0ExFjAUBgNVBAcMDU1vdW50YWluIFZpZXcxDTALBgNVBAoMBFdTTzIxEjAQBgNVBAMMCWxv"
			"Y2FsaG9zdDAeFw0xMDAyMTkwNzAyMjZaFw0zNTAyMTMwNzAyMjZaMFUxCzAJBgNVBAYTAlVTMQsw"
			"CQYDVQQIDAJDQTEWMBQGA1UEBwwNTW91bnRhaW4gVmlldzENMAsGA1UECgwEV1NPMjESMBAGA1UE"
			"AwwJbG9jYWxob3N0MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCUp/oV1vWc8/TkQSiAvTou"
			"sMzOM4asB2iltr2QKozni5aVFu818MpOLZIr8LMnTzWllJvvaA5RAAdpbECb+48FjbBe0hseUdN5"
			"HpwvnH/DW8ZccGvk53I6Orq7hLCv1ZHtuOCokghz/ATrhyPq+QktMfXnRS4HrKGJTzxaCcU7OQID"
			"AQABoxIwEDAOBgNVHQ8BAf8EBAMCBPAwDQYJKoZIhvcNAQEFBQADgYEAW5wPR7cr1LAdq+IrR44i"
			"QlRG5ITCZXY9hI0PygLP2rHANh+PYfTmxbuOnykNGyhM6FjFLbW2uZHQTY1jMrPprjOrmyK5sjJR"
			"O4d1DeGHT/YnIjs9JogRKv4XHECwLtIVdAbIdWHEtVZJyMSktcyysFcvuhPQK8Qc/E/Wq8uHSCo="
        )
    }
}


def get_idp_config(id, name=None):
    idp_metadata = et.parse("spid/spid-idp-metadata/spid-idp-%s.xml" % id).getroot()
    sso_path = './/{%s}SingleSignOnService[@Binding="%s"]' % \
               (SAML_METADATA_NAMESPACE, SAML_BINDING_REDIRECT_URN)
    slo_path = './/{%s}SingleLogoutService[@Binding="%s"]' % \
               (SAML_METADATA_NAMESPACE, SAML_BINDING_REDIRECT_URN)

    try:
        sso_location = idp_metadata.find(sso_path).attrib['Location']
    except (KeyError, AttributeError) as err:
        raise ValueError("Missing metadata SingleSignOnService for %r: %r" % (id, err))

    try:
        slo_location = idp_metadata.find(slo_path).attrib['Location']
    except (KeyError, AttributeError) as err:
        raise ValueError("Missing metadata SingleLogoutService for %r: %r" % (id, err))

    return {
        'name': name,
        'idp': {
            "entityId": idp_metadata.get("entityID"),
            "singleSignOnService": {
                "url": sso_location,
                "binding": SAML_BINDING_REDIRECT_URN
            },
            "singleLogoutService": {
                "url": slo_location,
                "binding": SAML_BINDING_REDIRECT_URN
            },
            "x509cert": idp_metadata.find(".//{%s}X509Certificate" % XML_SIGNATURE_NAMESPACE).text
        }
    }


class SpidConfig(AppConfig):
    name = 'spid'
    verbose_name = "SPID Authentication"

    identity_providers = {
        id: get_idp_config(id, name) for id, name in SPID_IDENTITY_PROVIDERS
    }

    @staticmethod
    def get_saml_settings(idp_id=None):
        if idp_id is None:
            return SPID_SAML_SETTINGS
        else:
            saml_settings = dict(SPID_SAML_SETTINGS)
            saml_settings.update({'idp': SpidConfig.identity_providers[idp_id]['idp']})
            return saml_settings