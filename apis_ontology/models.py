from apis_core.apis_entities.models import AbstractEntity
from django.utils.translation import gettext_lazy as _

from apis_core.generic.abc import GenericModel
from apis_core.history.models import VersionMixin
from apis_core.relations.models import Relation
from apis_core.apis_entities.abc import E53_Place
from django.db import models
from django_interval.fields import FuzzyDateParserField
from django_json_editor_field.fields import JSONEditorField


class Profession(GenericModel, models.Model):
    label = models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.label)


class OeaiBaseEntity:
    pass


class Person(OeaiBaseEntity, VersionMixin, AbstractEntity):
    PERIOD = [
        ("Byzanz", "Byzanz"),
        ("Griechen", "Griechen"),
        ("Kelten", "Kelten"),
        ("Provinzialrom", "Provinzialrom"),
        ("Römische Kaiserzeit", "Römische Kaiserzeit"),
        ("Römische Republik", "Römische Republik"),
    ]
    PERIOD_DETAIL = [
        ("Valentinianische Dynastie", "Valentinianische Dynastie"),
        ("Usurpator, Valens", "Usurpator, Valens"),
        ("Usurpator, Theodosius", "Usurpator, Theodosius"),
        ("Usurpator, Tetrarchie", "Usurpator, Tetrarchie"),
        ("Usurpator, Philippus Arabs", "Usurpator, Philippus Arabs"),
        ("Usurpator, Gallienus", "Usurpator, Gallienus"),
        ("Usurpator, Constantius II.", "Usurpator, Constantius II."),
        ("Theodosianische Dynastie", "Theodosianische Dynastie"),
        ("Tetrarchie", "Tetrarchie"),
        ("Soldatenkaisertum", "Soldatenkaisertum"),
        ("Severische Dynastie", "Palmyrenisches Reich"),
        ("Julisch-Claudische Dynastie", "Julisch-Claudische Dynastie"),
        ("Gallisches Sonderreich", "Gallisches Sonderreich"),
        ("Flavische Dynastie", "Flavische Dynastie"),
        ("Constantinische Dynastie", "Constantinische Dynastie"),
        ("Bürgerkrieg (68 - 69)", "Bürgerkrieg (68 - 69)"),
        ("Bürgerkrieg (193)", "Bürgerkrieg (193)"),
        (
            "Britannisches Sonderreich (286 ? - 297 ?)",
            "Britannisches Sonderreich (286 ? - 297 ?)",
        ),
        ("Adoptivkaisertum", "Adoptivkaisertum"),
        ("Boier", "Boier"),
    ]

    PERSON_TYPE = [
        ("Urheber, Unbekannt", "Urheber, Unbekannt"),
        ("archaeologist", "archaeologist"),
        ("architect", "architect"),
        ("artist", "artist"),
        ("collector", "collector"),
        ("excavation personnel", "excavation personnel"),
        ("explorer", "explorer"),
        ("institution personnel", "institution personnel"),
        ("mosaicist", "mosaicist"),
        ("painter", "painter"),
        ("person", "person"),
        ("potter", "potter"),
        ("sculptor", "sculptor"),
        ("vase painter", "vase painter"),
        ("Anonymous", "Anonymous"),
        ("processer", "processer"),
        ("modern person", "modern person"),
        ("historical person", "historical person"),
    ]

    label = models.CharField(max_length=255, help_text="PrefLabel in German")
    historical = models.BooleanField(default=True)
    profession = models.ForeignKey(
        Profession, on_delete=models.CASCADE, null=True, blank=True
    )
    period = models.CharField(choices=PERIOD, blank=True, null=True)
    period_detail = models.CharField(choices=PERIOD_DETAIL, blank=True, null=True)
    person_type = models.CharField(
        max_length=255, choices=PERSON_TYPE, blank=True, null=True
    )
    date_of_birth = FuzzyDateParserField(blank=True, null=True)
    date_of_death = FuzzyDateParserField(blank=True, null=True)
    schema = {
        "title": "Alternative Labels",
        "type": "array",
        "format": "table",
        "items": {
            "type": "object",
            "properties": {
                "label": {
                    "type": "string",
                    "pattern": "^.+$",
                    "options": {
                        "inputAttributes": {
                            "required": True,
                        },
                    },
                },
                "lang": {
                    "type": "string",
                    "enum": ["de", "en"],
                },
                "typ": {
                    "type": "string",
                    "enum": ["pref", "alt"],
                },
                "start": {
                    "type": "string",
                    "pattern": "^$|^\d\d\d\d$",
                    "options": {
                        "inputAttributes": {
                            "placeholder": "YYYY",
                        },
                        "containerAttributes": {
                            "class": "yearinput",
                        },
                    },
                },
                "end": {
                    "type": "string",
                    "pattern": "^$|^\d\d\d\d$",
                    "options": {
                        "inputAttributes": {
                            "placeholder": "YYYY",
                        },
                        "containerAttributes": {
                            "class": "yearinput",
                        },
                    },
                },
            },
        },
    }
    options = {
        "theme": "bootstrap4",
        "disable_collapse": True,
        "disable_edit_json": True,
        "disable_properties": True,
        "disable_array_reorder": True,
        "disable_array_delete_last_row": True,
        "disable_array_delete_all_rows": True,
        "prompt_before_delete": False,
    }

    alternative_labels = JSONEditorField(schema=schema, options=options, null=True)

    class Meta(VersionMixin.Meta, AbstractEntity.Meta):
        verbose_name = "Person"
        verbose_name_plural = "Persons"

    def __str__(self):
        return str(self.label)


class Institution(
    OeaiBaseEntity,
    VersionMixin,
    AbstractEntity,
):
    label = models.CharField(max_length=255, help_text="PrefLabel in German")
    hierarchy = models.CharField(max_length=100, null=True, blank=True)
    schema = {
        "title": "Alternative Labels",
        "type": "array",
        "format": "table",
        "items": {
            "type": "object",
            "properties": {
                "label": {
                    "type": "string",
                    "pattern": "^.+$",
                    "options": {
                        "inputAttributes": {
                            "required": True,
                        },
                    },
                },
                "lang": {
                    "type": "string",
                    "enum": ["de", "en", "fr", "it", "loc"],
                },
                "typ": {
                    "type": "string",
                    "enum": ["pref", "alt"],
                },
                "start": {
                    "type": "string",
                    "pattern": "^$|^\d\d\d\d$",
                    "options": {
                        "inputAttributes": {
                            "placeholder": "YYYY",
                        },
                        "containerAttributes": {
                            "class": "yearinput",
                        },
                    },
                },
                "end": {
                    "type": "string",
                    "pattern": "^$|^\d\d\d\d$",
                    "options": {
                        "inputAttributes": {
                            "placeholder": "YYYY",
                        },
                        "containerAttributes": {
                            "class": "yearinput",
                        },
                    },
                },
            },
        },
    }
    options = {
        "theme": "bootstrap4",
        "disable_collapse": True,
        "disable_edit_json": True,
        "disable_properties": True,
        "disable_array_reorder": True,
        "disable_array_delete_last_row": True,
        "disable_array_delete_all_rows": True,
        "prompt_before_delete": False,
    }

    alternative_labels = JSONEditorField(schema=schema, options=options, null=True)

    class Meta(VersionMixin.Meta, AbstractEntity.Meta):
        verbose_name = "Institution"
        verbose_name_plural = "Institutions"

    def __str__(self):
        return str(self.label)


class Place(OeaiBaseEntity, VersionMixin, E53_Place, AbstractEntity):
    class Meta(VersionMixin.Meta, E53_Place.Meta, AbstractEntity.Meta):
        verbose_name = "Place"
        verbose_name_plural = "Places"


##################
#
# Relations
#
#################


class EngagedIn(Relation):
    TYPE = [("employed", "employed"), ("hired", "hired"), ("leading", "leading")]

    subj_model = Person
    obj_model = Institution
    typen = models.CharField(choices=TYPE)
    begin = FuzzyDateParserField(blank=True)
    end = FuzzyDateParserField(blank=True)

    @classmethod
    def name(cls) -> str:
        return "engaged in"

    @classmethod
    def reverse_name(cls) -> str:
        return "engages"

    class Meta:
        verbose_name = _("engaged in")
        verbose_name_plural = _("engaged in")


class LocatedIn(Relation):
    subj_model = Institution
    obj_model = Place
    begin = FuzzyDateParserField(blank=True)
    end = FuzzyDateParserField(blank=True)

    @classmethod
    def name(cls) -> str:
        return "located in"

    @classmethod
    def reverse_name(cls) -> str:
        return "includes"

    class Meta:
        verbose_name = _("located in")
        verbose_name_plural = _("located in")


class Includes(Relation):
    subj_model = Place
    obj_model = Place
    begin = FuzzyDateParserField(blank=True)
    end = FuzzyDateParserField(blank=True)

    @classmethod
    def name(cls) -> str:
        return "includes"

    @classmethod
    def reverse_name(cls) -> str:
        return "included in"

    class Meta:
        verbose_name = _("includes")
        verbose_name_plural = _("include")


class Contains(Relation):
    subj_model = Institution
    obj_model = Institution
    begin = FuzzyDateParserField(blank=True)
    end = FuzzyDateParserField(blank=True)

    @classmethod
    def name(cls) -> str:
        return "contains"

    @classmethod
    def reverse_name(cls) -> str:
        return "is contained in"

    class Meta:
        verbose_name = _("contains")
        verbose_name_plural = _("contain")
