from apis_core.apis_entities.models import Uri
from django.core.management.base import CommandError
from apis_ontology.management.commands.import_csv import Command as ImportCsvCommand
from apis_ontology.models import Profession


class Command(ImportCsvCommand):
    help = "Import person data from a CSV file"

    def import_row(self, row):
        """
        Process a single row from the CSV file to import a person.

        Args:
            row (dict): A dictionary representing a row from the CSV file,
                        with column names as keys.
        """
        try:
            # Example implementation - replace with your actual model and field mapping
            from apis_ontology.models import Person

            # Check for required fields
            required_fields = ["skos:prefLabel @de"]
            for field in required_fields:
                if field not in row or not row[field]:
                    raise ValueError(f"Missing required field: {field}")
            occ = None
            if "skos:broader occupation" in row.keys():
                if len(row.get("skos:broader occupation")) > 0:
                    occ, c = Profession.objects.get_or_create(
                        label=row.get("skos:broader occupation")
                    )
            alt_label = []
            for alt in [
                "skos:altLabel @de",
                "skos:altLabel @de 2",
                "skos:altLabel @de 3",
                "skos:altLabel @de 4",
                "skos:altLabel @de 5",
                "skos:altLabel @en",
                "skos:prefLabel @en",
            ]:
                if alt in row.keys():
                    if len(row[alt]) > 0:
                        alt_label.append(
                            {
                                "label": row[alt],
                                "lang": "de" if "@de" in row[alt] else "en",
                                "typ": "alt" if "altLabel" in row[alt] else "pref",
                            }
                        )

            # Create a new person for each row
            date_of_birth = None
            date_of_death = None
            if "skos:scope" in row.keys():
                if len(row["skos:scope"]) > 0:
                    date_of_birth, date_of_death = row["skos:scope"].split("-")
            person = Person.objects.create(
                label=row["skos:prefLabel @de"],
                person_type=row.get("skos:broader", ""),
                profession=occ,
                date_of_death=date_of_death,
                date_of_birth=date_of_birth,
                historical=row["skos:broader"] == "historical person",
                alternative_labels=alt_label,
                period=row.get("skos:broader time", None),
                period_detail=row.get("skos:broader time02", None),
                # Add more fields as needed
            )
            if "skos:exactMatch" in row.keys():
                if len(row.get("skos:exactMatch")) > 0:
                    Uri.objects.create(
                        content_object=person, uri=row.get("skos:exactMatch")
                    )

            self.stdout.write(f"Created person: {person.label}")
            self.logger.info(f"Created person: {person.label}")

            return person

        except Exception as e:
            # Re-raise the exception to be caught by the parent command
            self.logger.error(f"Error importing person: {str(e)}")
            raise CommandError(f"Error importing person: {str(e)}")
