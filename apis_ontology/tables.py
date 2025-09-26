from apis_core.apis_entities.tables import AbstractEntityTable
from django.utils.html import format_html


class OeaiBaseEntityTable(AbstractEntityTable):
    def render_uris(self, value):
        return format_html(", ".join([f'<a href="{v}">{v}</a>' for v in value]))
