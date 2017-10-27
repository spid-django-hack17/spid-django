import random

from django import template
from ..apps import SpidConfig

register = template.Library()

SPID_BUTTON_SIZES = {'small', 'medium', 'large', 'xlarge'}


@register.inclusion_tag("spid/spid_button.html")
def show_idp_list(size='medium'):
    if size not in SPID_BUTTON_SIZES:
        raise ValueError("argument 'size': value %r not in %r." % (size, SPID_BUTTON_SIZES))

    spid_idp_list = [
        {'id': k, 'name': v['name']}
        for k, v in SpidConfig.identity_providers.items()
    ]
    random.shuffle(spid_idp_list)
    return {
        'spid_button_size': size,
        'spid_button_size_short': size[0] if size != 'xlarge' else size[:2],
        'spid_idp_list': spid_idp_list
    }
