from apis_acdhch_default_settings.settings import *  # noqa: F403

# INSTALLED_APPS.remove("apis_ontology")
ROOT_URLCONF = "apis_ontology.urls"

DEBUG = True

INSTALLED_APPS += [  # noqa: F405
    "django.contrib.postgres",
    #    "apis_core.collections",
    # "apis_core.history",
    "django_json_editor_field",
]
INSTALLED_APPS.remove("apis_ontology")
INSTALLED_APPS.insert(0, "apis_ontology")

APIS_BASE_URI = "https://vocabs-oeai.acdh-ch-dev.oeaw.ac.at"
