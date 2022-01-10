ALLOWED_HOSTS = ["*"]

# Modules in use, commented modules that you won't use
MODULES = [
    'authentication',
    'base',
    'booth',
    'census',
    'mixnet',
    'postproc',
    'store',
    'visualizer',
    'voting',
]

BASEURL = 'https://decide-penyagolosa-3.herokuapp.com'

APIS = {
    'authentication': BASEURL,
    'base': BASEURL,
    'booth': BASEURL,
    'census': BASEURL,
    'mixnet': BASEURL,
    'postproc': BASEURL,
    'store': BASEURL,
    'visualizer': BASEURL,
    'voting': BASEURL,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd8k4jad1ha5rc1',
        'USER': 'uhczrelzeornwa',
        'PASSWORD': 'cc3dfc2bdb9e552e0ce3446120db9fcb4232a96593c350f08db29ba47048227a',
        'HOST': 'ec2-52-208-221-89.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}

# number of bits for the key, all auths should use the same number of bits


KEYBITS = 256
