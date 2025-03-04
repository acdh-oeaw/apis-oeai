from apis_core.apis_entities.models import Uri
from django.core.management.base import CommandError
from apis_ontology.management.commands.import_csv import Command as ImportCsvCommand
from apis_ontology.models import (
    Contains,
    Institution,
    LocatedIn,
    Place,
    Profession,
    Includes,
    Place,
)


def get_lang(col):
    match col:
        case col if "@de" in col:
            return "de"
        case col if "@en" in col:
            return col
        case col if "@fr" in col:
            return "fr"
        case col if "@esp" in col:
            return "es"
        case col if "@ita" in col:
            return "it"
        case col if "@Local" in col:
            return "loc"
    return None


def proc_places(row, inst):
    land = False
    if row.get("Land", None):
        land, c = Place.objects.get_or_create(
            label=row.get("Land"), defaults={"feature_code": "PCL"}
        )
    lev1 = row.get("skos:broader name1", None)
    lev2 = row.get("skos:broader name2", None)
    city = False
    inst1 = False
    if lev1.strip().lower() == lev2.strip().lower():
        city, c = Place.objects.get_or_create(label=lev1.strip())
    elif lev1 and lev2:
        inst1, c = Institution.objects.get_or_create(label=lev1.strip())
        city, c = Place.objects.get_or_create(label=lev2.strip())
        Contains.objects.create(subj=inst1, obj=inst)
        LocatedIn.objects.create(subj=inst1, obj=city)
    elif lev1 and not lev2:
        city, c = Place.objects.get_or_create(label=lev1.strip())
    elif lev2 and not lev1:
        city, c = Place.objects.get_or_create(label=lev2.strip())
    if not inst1 and city:
        LocatedIn.objects.create(subj=inst, obj=city)
    if land and city:
        from django.contrib.contenttypes.models import ContentType

        place_ct = ContentType.objects.get_for_model(Place)
        Includes.objects.get_or_create(
            subj_object_id=land.pk,
            obj_object_id=city.pk,
            subj_content_type=place_ct,
            obj_content_type=place_ct,
        )
    return True


class Command(ImportCsvCommand):
    help = "Import person data from a CSV file"

    def import_row(self, row):
        """
        Process a single row from the CSV file to import a institution.

        Args:
            row (dict): A dictionary representing a row from the CSV file,
                        with column names as keys.
        """
        try:
            # Example implementation - replace with your actual model and field mapping

            # Check for required fields
            required_fields = ["skos:prefLabel @de"]
            for field in required_fields:
                if field not in row or not row[field]:
                    raise ValueError(f"Missing required field: {field}")
            alt_label = []
            for alt in [
                "skos:altLabel @de",
                "skos:altLabel @de 2",
                "skos:altLabel @en",
                "skos:prefLabel @en",
                "skos:prefLabel @fr",
                "skos:altLabel @fr",
                "skos:prefLabel @esp",
                "skos:prefLable@ita",
                "skos:prefLabel@Local Language",
                "skos:altLabel@Local Language",
            ]:
                if alt in row.keys():
                    if len(row[alt]) > 0:
                        alt_label.append(
                            {
                                "label": row[alt],
                                "lang": get_lang(alt),
                                "typ": "alt" if "altLabel" in alt else "pref",
                            }
                        )

            # Create a new person for each row
            inst = Institution.objects.create(
                label=row["skos:prefLabel @de"],
                alternative_labels=alt_label,
                abbreviation=row.get("Abkürzen", None),
                easydb4_reference=row.get("easydb4_reference", None),
                hierarchy=row.get("hierarchy", None),
                system_object_id=row.get("_system_object_id", None),
                # Add more fields as needed
            )
            for header in ["Link-exact", "Link-related"]:
                if header in row.keys():
                    if len(row.get(header)) > 0:
                        Uri.objects.create(content_object=inst, uri=row.get(header))
            proc_places(row, inst)

            self.stdout.write(f"Created institution: {inst.label}")
            self.logger.info(f"Created institution: {inst.label}")

            return inst

        except Exception as e:
            # Re-raise the exception to be caught by the parent command
            self.logger.error(f"Error importing institution: {str(e)}")
            raise CommandError(f"Error importing person: {str(e)}")
