import os

from django.utils.translation import ugettext_lazy as _
{% if use_syslog %}
from logging.handlers import SysLogHandler
{% endif %}

from openstack_dashboard import exceptions

DEBUG = {{ debug }}
TEMPLATE_DEBUG = DEBUG

# Required for Django 1.5.
# If horizon is running in production (DEBUG is False), set this
# with the list of host/domain names that the application can serve.
# For more information see:
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
#ALLOWED_HOSTS = ['horizon.example.com', ]

# Set SSL proxy settings:
# For Django 1.4+ pass this header from the proxy after terminating the SSL,
# and don't forget to strip it from the client's request.
# For more information see:
# https://docs.djangoproject.com/en/1.4/ref/settings/#secure-proxy-ssl-header
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

# If Horizon is being served through SSL, then uncomment the following two
# settings to better secure the cookies from security exploits
#CSRF_COOKIE_SECURE = True
#SESSION_COOKIE_SECURE = True
{% if ssl_configured %}
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
{% endif %}

# A method to supersede the token timeout with a shorter dashboard session
# timeout in seconds.
SESSION_TIMEOUT = {{ session_timeout }}

# Overrides for OpenStack API versions. Use this setting to force the
# OpenStack dashboard to use a specfic API version for a given service API.
# NOTE: The version should be formatted as it appears in the URL for the
# service API. For example, The identity service APIs have inconsistent
# use of the decimal point, so valid options would be "2.0" or "3".
# OPENSTACK_API_VERSIONS = {
#     "identity": 3
# }

# Set this to True if running on multi-domain model. When this is enabled, it
# will require user to enter the Domain name in addition to username for login.
# OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = False

# Overrides the default domain used when running on single-domain model
# with Keystone V3. All entities will be created in the default domain.
# OPENSTACK_KEYSTONE_DEFAULT_DOMAIN = 'Default'

# Set Console type:
# valid options would be "AUTO", "VNC" or "SPICE"
# CONSOLE_TYPE = "AUTO"

# Default OpenStack Dashboard configuration.
HORIZON_CONFIG = {
    'dashboards': ('project', 'admin', 'settings',),
    'default_dashboard': 'project',
    'user_home': 'openstack_dashboard.views.get_user_home',
    'ajax_queue_limit': 10,
    'auto_fade_alerts': {
        'delay': 3000,
        'fade_duration': 1500,
        'types': ['alert-success', 'alert-info']
    },
    'help_url': "http://docs.openstack.org",
    'exceptions': {'recoverable': exceptions.RECOVERABLE,
                   'not_found': exceptions.NOT_FOUND,
                   'unauthorized': exceptions.UNAUTHORIZED},
}

# Specify a regular expression to validate user passwords.
# HORIZON_CONFIG["password_validator"] = {
#     "regex": '.*',
#     "help_text": _("Your password does not meet the requirements.")
# }

# Disable simplified floating IP address management for deployments with
# multiple floating IP pools or complex network requirements.
# HORIZON_CONFIG["simple_ip_management"] = False

# Turn off browser autocompletion for the login form if so desired.
# HORIZON_CONFIG["password_autocomplete"] = "off"
{% if allow_password_autocompletion %}
HORIZON_CONFIG["password_autocomplete"] = "on"
{% endif %}

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))

# Set custom secret key:
# You can either set it to a specific value or you can let horizion generate a
# default secret key that is unique on this machine, e.i. regardless of the
# amount of Python WSGI workers (if used behind Apache+mod_wsgi): However, there
# may be situations where you would want to set this explicitly, e.g. when
# multiple dashboard instances are distributed on different machines (usually
# behind a load-balancer). Either you have to make sure that a session gets all
# requests routed to the same dashboard instance or you set the same SECRET_KEY
# for all of them.

SECRET_KEY = "{{ secret }}"

# We recommend you use memcached for development; otherwise after every reload
# of the django development server, you will have to login again. To use
# memcached set CACHES to something like
CACHES = {
   'default': {
       'BACKEND' : 'django.core.cache.backends.memcached.MemcachedCache',
       'LOCATION' : '127.0.0.1:11211',
   }
}

# Send email to the console by default
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Or send them to /dev/null
#EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# Configure these for your outgoing email host
# EMAIL_HOST = 'smtp.my-company.com'
# EMAIL_PORT = 25
# EMAIL_HOST_USER = 'djangomail'
# EMAIL_HOST_PASSWORD = 'top-secret!'

# For multiple regions uncomment this configuration, and add (endpoint, title).
# AVAILABLE_REGIONS = [
#     ('http://cluster1.example.com:5000/v2.0', 'cluster1'),
#     ('http://cluster2.example.com:5000/v2.0', 'cluster2'),
# ]
{% if regions|length > 1 -%}
AVAILABLE_REGIONS = [
{% for region in regions -%}
    ('{{ region.endpoint }}', '{{ region.title }}'),
{% endfor -%}
]
{% endif -%}

OPENSTACK_HOST = "{{ ks_host }}"
OPENSTACK_KEYSTONE_URL = "{{ ks_protocol }}://%s:{{ ks_port }}/v2.0" % OPENSTACK_HOST
OPENSTACK_KEYSTONE_DEFAULT_ROLE = "{{ default_role }}"

# Disable SSL certificate checks (useful for self-signed certificates):
# OPENSTACK_SSL_NO_VERIFY = True

# The CA certificate to use to verify SSL connections
# OPENSTACK_SSL_CACERT = '/path/to/cacert.pem'

# The OPENSTACK_KEYSTONE_BACKEND settings can be used to identify the
# capabilities of the auth backend for Keystone.
# If Keystone has been configured to use LDAP as the auth backend then set
# can_edit_user to False and name to 'ldap'.
#
# TODO(tres): Remove these once Keystone has an API to identify auth backend.
OPENSTACK_KEYSTONE_BACKEND = {
    'name': 'native',
    'can_edit_user': True,
    'can_edit_group': True,
    'can_edit_project': True,
    'can_edit_domain': True,
    'can_edit_role': True
}

OPENSTACK_HYPERVISOR_FEATURES = {
    'can_set_mount_point': False,
    'can_set_password': False,
}

# The OPENSTACK_NEUTRON_NETWORK settings can be used to enable optional
# services provided by neutron. Options currenly available are load
# balancer service, security groups, quotas.
OPENSTACK_NEUTRON_NETWORK = {
    'enable_lb': {{ neutron_network_lb }},
    'enable_quotas': True,
    'enable_security_group': True,
    'enable_firewall': {{ neutron_network_firewall }},
    'enable_vpn': {{ neutron_network_vpn }},
    # The profile_support option is used to detect if an external router can be
    # configured via the dashboard. When using specific plugins the
    # profile_support can be turned on if needed.
    #'profile_support': None,
    #'profile_support': 'cisco', # Example of value set to support Cisco
    {% if support_profile -%}
    'profile_support': '{{ support_profile }}',
    {% else -%}
    'profile_support': None,
    {% endif -%}
}

# The OPENSTACK_IMAGE_BACKEND settings can be used to customize features
# in the OpenStack Dashboard related to the Image service, such as the list
# of supported image formats.
OPENSTACK_IMAGE_BACKEND = {
    'image_formats': [
        ('', ''),
        ('aki', _('AKI - Amazon Kernel Image')),
        ('ami', _('AMI - Amazon Machine Image')),
        ('ari', _('ARI - Amazon Ramdisk Image')),
        ('iso', _('ISO - Optical Disk Image')),
        ('qcow2', _('QCOW2 - QEMU Emulator')),
        ('raw', _('Raw')),
        ('vdi', _('VDI')),
        ('vhd', _('VHD')),
        ('vmdk', _('VMDK'))
    ]
}

# The IMAGE_CUSTOM_PROPERTY_TITLES settings is used to customize the titles for
# image custom property attributes that appear on image detail pages.
IMAGE_CUSTOM_PROPERTY_TITLES = {
    "architecture": _("Architecture"),
    "kernel_id": _("Kernel ID"),
    "ramdisk_id": _("Ramdisk ID"),
    "image_state": _("Euca2ools state"),
    "project_id": _("Project ID"),
    "image_type": _("Image Type")
}

# OPENSTACK_ENDPOINT_TYPE specifies the endpoint type to use for the endpoints
# in the Keystone service catalog. Use this setting when Horizon is running
# external to the OpenStack environment. The default is 'publicURL'.
#OPENSTACK_ENDPOINT_TYPE = "publicURL"
{% if primary_endpoint -%}
OPENSTACK_ENDPOINT_TYPE = "{{ primary_endpoint }}"
{% endif -%}

# SECONDARY_ENDPOINT_TYPE specifies the fallback endpoint type to use in the
# case that OPENSTACK_ENDPOINT_TYPE is not present in the endpoints
# in the Keystone service catalog. Use this setting when Horizon is running
# external to the OpenStack environment. The default is None.  This
# value should differ from OPENSTACK_ENDPOINT_TYPE if used.
#SECONDARY_ENDPOINT_TYPE = "publicURL"
{% if secondary_endpoint -%}
SECONDARY_ENDPOINT_TYPE = "{{ secondary_endpoint }}"
{% endif -%}

# The number of objects (Swift containers/objects or images) to display
# on a single page before providing a paging element (a "more" link)
# to paginate results.
API_RESULT_LIMIT = {{ api_result_limit }}
API_RESULT_PAGE_SIZE = 20

# The timezone of the server. This should correspond with the timezone
# of your entire OpenStack installation, and hopefully be in UTC.
TIME_ZONE = "UTC"

# When launching an instance, the menu of available flavors is
# sorted by RAM usage, ascending.  Provide a callback method here
# (and/or a flag for reverse sort) for the sorted() method if you'd
# like a different behaviour.  For more info, see
# http://docs.python.org/2/library/functions.html#sorted
# CREATE_INSTANCE_FLAVOR_SORT = {
#     'key': my_awesome_callback_method,
#     'reverse': False,
# }

# The Horizon Policy Enforcement engine uses these values to load per service
# policy rule files. The content of these files should match the files the
# OpenStack services are using to determine role based access control in the
# target installation.

# Path to directory containing policy.json files
#POLICY_FILES_PATH = os.path.join(ROOT_PATH, "conf")
# Map of local copy of service policy files
#POLICY_FILES = {
#    'identity': 'keystone_policy.json',
#    'compute': 'nova_policy.json'
#}

# Trove user and database extension support. By default support for
# creating users and databases on database instances is turned on.
# To disable these extensions set the permission here to something
# unusable such as ["!"].
# TROVE_ADD_USER_PERMS = []
# TROVE_ADD_DATABASE_PERMS = []

LOGGING = {
    'version': 1,
    # When set to True this will disable all logging except
    # for loggers specified in this configuration dictionary. Note that
    # if nothing is specified here and disable_existing_loggers is True,
    # django.db.backends will still log unless it is disabled explicitly.
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            # Set the level to "DEBUG" for verbose output logging.
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        {% if use_syslog %}
        'syslog': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
        }
        {% endif %}
    },
    'loggers': {
        # Logging from django.db.backends is VERY verbose, send to null
        # by default.
        'django.db.backends': {
            'handlers': ['null'],
            'propagate': False,
        },
        'requests': {
            'handlers': ['null'],
            'propagate': False,
        },
        'horizon': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'propagate': False,
        },
        'openstack_dashboard': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'propagate': False,
        },
        'openstack_auth': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'propagate': False,
        },
        'novaclient': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'propagate': False,
        },
        'cinderclient': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'propagate': False,
        },
        'keystoneclient': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'propagate': False,
        },
        'glanceclient': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'propagate': False,
        },
        'heatclient': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'propagate': False,
        },
        'nose.plugins.manager': {
            {% if use_syslog %}
            'handlers': ['syslog'],
            {% else %}
            'handlers': ['console'],
            {% endif %}
            'propagate': False,
        }
    }
}

SECURITY_GROUP_RULES = {
    'all_tcp': {
        'name': 'ALL TCP',
        'ip_protocol': 'tcp',
        'from_port': '1',
        'to_port': '65535',
    },
    'all_udp': {
        'name': 'ALL UDP',
        'ip_protocol': 'udp',
        'from_port': '1',
        'to_port': '65535',
    },
    'all_icmp': {
        'name': 'ALL ICMP',
        'ip_protocol': 'icmp',
        'from_port': '-1',
        'to_port': '-1',
    },
    'ssh': {
        'name': 'SSH',
        'ip_protocol': 'tcp',
        'from_port': '22',
        'to_port': '22',
    },
    'smtp': {
        'name': 'SMTP',
        'ip_protocol': 'tcp',
        'from_port': '25',
        'to_port': '25',
    },
    'dns': {
        'name': 'DNS',
        'ip_protocol': 'tcp',
        'from_port': '53',
        'to_port': '53',
    },
    'http': {
        'name': 'HTTP',
        'ip_protocol': 'tcp',
        'from_port': '80',
        'to_port': '80',
    },
    'pop3': {
        'name': 'POP3',
        'ip_protocol': 'tcp',
        'from_port': '110',
        'to_port': '110',
    },
    'imap': {
        'name': 'IMAP',
        'ip_protocol': 'tcp',
        'from_port': '143',
        'to_port': '143',
    },
    'ldap': {
        'name': 'LDAP',
        'ip_protocol': 'tcp',
        'from_port': '389',
        'to_port': '389',
    },
    'https': {
        'name': 'HTTPS',
        'ip_protocol': 'tcp',
        'from_port': '443',
        'to_port': '443',
    },
    'smtps': {
        'name': 'SMTPS',
        'ip_protocol': 'tcp',
        'from_port': '465',
        'to_port': '465',
    },
    'imaps': {
        'name': 'IMAPS',
        'ip_protocol': 'tcp',
        'from_port': '993',
        'to_port': '993',
    },
    'pop3s': {
        'name': 'POP3S',
        'ip_protocol': 'tcp',
        'from_port': '995',
        'to_port': '995',
    },
    'ms_sql': {
        'name': 'MS SQL',
        'ip_protocol': 'tcp',
        'from_port': '1443',
        'to_port': '1443',
    },
    'mysql': {
        'name': 'MYSQL',
        'ip_protocol': 'tcp',
        'from_port': '3306',
        'to_port': '3306',
    },
    'rdp': {
        'name': 'RDP',
        'ip_protocol': 'tcp',
        'from_port': '3389',
        'to_port': '3389',
    },
}

FLAVOR_EXTRA_KEYS = {
    'flavor_keys': [
        ('quota:read_bytes_sec', _('Quota: Read bytes')),
        ('quota:write_bytes_sec', _('Quota: Write bytes')),
        ('quota:cpu_quota', _('Quota: CPU')),
        ('quota:cpu_period', _('Quota: CPU period')),
        ('quota:inbound_average', _('Quota: Inbound average')),
        ('quota:outbound_average', _('Quota: Outbound average')),
    ]
}

{% if ubuntu_theme %}
# Enable the Ubuntu theme if it is present.
try:
    from ubuntu_theme import *
except ImportError:
    pass
{% endif %}

WEBROOT = '{{ webroot }}'

# Default Ubuntu apache configuration uses /horizon as the application root.
# Configure auth redirects here accordingly.
{% if webroot == "/" %}
LOGIN_URL='/auth/login/'
LOGOUT_URL='/auth/logout/'
{% else %}
LOGIN_URL='{{ webroot }}/auth/login/'
LOGOUT_URL='{{ webroot }}/auth/logout/'
{% endif %}
LOGIN_REDIRECT_URL='{{ webroot }}'

# The Ubuntu package includes pre-compressed JS and compiled CSS to allow
# offline compression by default.  To enable online compression, install
# the node-less package and enable the following option.
COMPRESS_OFFLINE = {{ compress_offline }}

# By default, validation of the HTTP Host header is disabled.  Production
# installations should have this set accordingly.  For more information
# see https://docs.djangoproject.com/en/dev/ref/settings/.
ALLOWED_HOSTS = '*'

{% if password_retrieve %}
OPENSTACK_ENABLE_PASSWORD_RETRIEVE = True
{% endif %}

{{ settings|join('\n\n') }}
