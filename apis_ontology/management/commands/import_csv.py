import csv
import os
import logging
import datetime
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Import data from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file to import")
        parser.add_argument(
            "--delimiter", type=str, default=",", help='CSV delimiter (default: ",")'
        )
        parser.add_argument(
            "--encoding",
            type=str,
            default="utf-8",
            help="File encoding (default: utf-8)",
        )
        parser.add_argument(
            "--log-file",
            type=str,
            help="Path to the log file (default: import_<timestamp>.log in the same directory as the CSV)",
        )

    def handle(self, *args, **options):
        csv_file_path = options["csv_file"]
        delimiter = options["delimiter"]
        encoding = options["encoding"]

        # Setup logging
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = options.get("log_file")
        if not log_file:
            # Default log file in the same directory as the CSV
            csv_dir = os.path.dirname(os.path.abspath(csv_file_path))
            csv_filename = os.path.basename(csv_file_path)
            log_file = os.path.join(
                csv_dir, f"import_{os.path.splitext(csv_filename)[0]}_{timestamp}.log"
            )

        # Configure logger
        self.logger = logging.getLogger("csv_import")
        self.logger.setLevel(logging.INFO)

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        # Add handler to logger
        self.logger.addHandler(file_handler)

        self.logger.info(f"Starting import of {csv_file_path}")
        self.stdout.write(f"Logging to {log_file}")

        if not os.path.exists(csv_file_path):
            error_msg = f"File does not exist: {csv_file_path}"
            self.logger.error(error_msg)
            raise CommandError(error_msg)

        try:
            with open(csv_file_path, "r", encoding=encoding) as csv_file:
                reader = csv.DictReader(csv_file, delimiter=delimiter)

                # Get total number of rows for progress reporting
                total_rows = (
                    sum(1 for _ in open(csv_file_path, "r", encoding=encoding)) - 1
                )

                # Reset file pointer
                csv_file.seek(0)
                next(reader)  # Skip header row

                processed = 0
                success = 0
                errors = 0

                for row in reader:
                    processed += 1

                    # Show progress
                    if processed % 100 == 0 or processed == total_rows:
                        progress_msg = f"Processing row {processed}/{total_rows}..."
                        self.stdout.write(progress_msg)
                        self.logger.info(progress_msg)

                    try:
                        # Call the import_row function with the current row
                        self.import_row(row)
                        success += 1
                    except Exception as e:
                        errors += 1
                        error_msg = f"Error processing row {processed}: {str(e)}"
                        self.stderr.write(self.style.ERROR(error_msg))

                        # Log detailed error information
                        self.logger.error(error_msg)
                        self.logger.error(f"Row data: {row}")

                        # Optionally log the full traceback for debugging
                        import traceback

                        self.logger.error(f"Traceback: {traceback.format_exc()}")

                summary_msg = f"Import completed. Processed: {processed}, Success: {success}, Errors: {errors}"
                self.stdout.write(self.style.SUCCESS(summary_msg))
                self.logger.info(summary_msg)

        except Exception as e:
            error_msg = f"Error reading CSV file: {str(e)}"
            self.logger.error(error_msg)
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            raise CommandError(error_msg)
        finally:
            # Close all handlers to ensure log file is properly saved
            for handler in self.logger.handlers:
                handler.close()
                self.logger.removeHandler(handler)

    def import_row(self, row):
        """
        Process a single row from the CSV file.
        Override this method in a subclass to implement specific import logic.

        Args:
            row (dict): A dictionary representing a row from the CSV file,
                        with column names as keys.
        """
        # This is a placeholder implementation
        # In a real application, you would implement your specific import logic here
        message = f"Would import: {row}"
        self.stdout.write(message)
        self.logger.info(message)

        # Example implementation:
        # from apis_ontology.models import YourModel
        # obj = YourModel(
        #     field1=row['column1'],
        #     field2=row['column2'],
        #     # ...
        # )
        # obj.save()
        # self.logger.info(f"Successfully imported {obj}")
