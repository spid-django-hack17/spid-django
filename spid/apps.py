from django.conf import settings
from django.apps import AppConfig


SPID_NAME_FORMAT = "urn:oasis:names:tc:SAML:2.0:attrname-format:basic"

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


class SpidConfig(AppConfig):
    name = 'spid'
    verbose_name = "SPID Authentication"

    saml_settings = dict(SPID_SAML_SETTINGS)
