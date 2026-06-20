"""
CLI entry point for InvoiceXtract
"""

import logging
from pathlib import Path
from typing import Optional

import click

from invoicextract import InvoiceExtractor, __version__
from invoicextract.config import LOG_FORMAT, LOG_LEVEL
from invoicextract.exporters.csv_exporter import CSVExporter
from invoicextract.exporters.excel_exporter import ExcelExporter
from invoicextract.exporters.json_exporter import JSONExporter

# Setup logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version=__version__)
def cli():
    """InvoiceXtract - Automated invoice data extraction"""
    pass


@cli.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["csv", "json", "excel"], case_sensitive=False),
    default="csv",
    help="Export format (default: csv)",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def extract(input_path: str, output: Optional[str], format: str, verbose: bool):
    """Extract data from invoice(s)"""

    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info(f"Starting extraction from: {input_path}")

    try:
        # Initialize extractor
        extractor = InvoiceExtractor()

        # Handle single file or directory
        input_path_obj = Path(input_path)
        invoices = []

        if input_path_obj.is_file():
            invoice = extractor.extract(input_path)
            invoices.append(invoice)
            logger.info(f"Extracted invoice #{invoice.invoice_number}")
        elif input_path_obj.is_dir():
            for file_path in input_path_obj.glob("*.pdf"):
                try:
                    invoice = extractor.extract(str(file_path))
                    invoices.append(invoice)
                    logger.info(f"Extracted: {file_path.name}")
                except Exception as e:
                    logger.error(f"Failed to extract {file_path.name}: {e}")

        # Export results
        if not invoices:
            logger.warning("No invoices extracted")
            return

        # Determine output path
        if not output:
            output = f"invoices.{format}"

        # Select exporter
        exporters = {
            "csv": CSVExporter(),
            "json": JSONExporter(),
            "excel": ExcelExporter(),
        }

        exporter = exporters[format.lower()]
        exporter.export(invoices, output)

        logger.info(f"Successfully exported {len(invoices)} invoice(s) to {output}")
        click.echo(f"✓ Extracted {len(invoices)} invoice(s) → {output}")

    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@cli.command()
def info():
    """Display system and configuration information"""
    click.echo(f"InvoiceXtract v{__version__}")
    click.echo("\nConfiguration:")

    from invoicextract.config import (
        LOG_LEVEL,
        MAX_FILE_SIZE_MB,
        OCR_DPI,
        OCR_ENGINE,
        OCR_LANGUAGE,
    )

    click.echo(f"  OCR Engine: {OCR_ENGINE}")
    click.echo(f"  OCR Language: {OCR_LANGUAGE}")
    click.echo(f"  OCR DPI: {OCR_DPI}")
    click.echo(f"  Max File Size: {MAX_FILE_SIZE_MB}MB")
    click.echo(f"  Log Level: {LOG_LEVEL}")


if __name__ == "__main__":
    cli()
