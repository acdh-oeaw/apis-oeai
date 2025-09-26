from apis_core.uris.models import Uri
from django.db.models import OuterRef
from django.contrib.postgres.expressions import ArraySubquery


uris = (
    Uri.objects.filter(object_id=OuterRef("pk"))
    .exclude(uri__contains="vocabs-oeai")
    .values_list("uri", flat=True)
)


def OeaiBaseEntityListViewQueryset(*args):
    qs = args[0].annotate(uris=ArraySubquery(uris))
    return qs
