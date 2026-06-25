import logging
import tempfile
from pathlib import Path

import gradio as gr
import pandas as pd

from invoicextract import InvoiceExtractor
from invoicextract.exporters.csv_exporter import CSVExporter
from invoicextract.exporters.excel_exporter import ExcelExporter
from invoicextract.exporters.json_exporter import JSONExporter

logger = logging.getLogger(__name__)


def process_files(files):
    if not files:
        return (
            pd.DataFrame(),
            pd.DataFrame(),
            "No files uploaded.",
            "",
            [],
        )

    extractor = InvoiceExtractor()
    invoices = []
    error_messages = []

    for f in files:
        try:
            invoice = extractor.extract(f.name)
            invoices.append(invoice)
        except Exception as e:
            error_messages.append(f"{Path(f.name).name}: {e}")

    if not invoices and error_messages:
        return (
            pd.DataFrame(),
            pd.DataFrame(),
            "\n\n".join(error_messages),
            "",
            [],
        )

    summary_rows = []
    for inv in invoices:
        total = f"{inv.total_amount:.2f} {inv.currency}" if inv.total_amount is not None else "-"
        subtotal = f"{inv.subtotal:.2f}" if inv.subtotal is not None else "-"
        tax = f"{inv.tax_amount:.2f}" if inv.tax_amount is not None else "-"
        due = inv.due_date or "-"
        terms = inv.payment_terms or "-"
        summary_rows.append(
            {
                "Invoice #": inv.invoice_number or "-",
                "Vendor": inv.vendor_name or "-",
                "Customer": inv.customer_name or "-",
                "Date": inv.invoice_date or "-",
                "Due Date": due,
                "Subtotal": subtotal,
                "Tax": tax,
                "Total": total,
                "Payment Terms": terms,
                "Valid": "Yes" if inv.is_valid else "No",
                "File": Path(inv.source_file).name if inv.source_file else "-",
            }
        )
    summary_df = pd.DataFrame(summary_rows)

    item_rows = []
    for inv in invoices:
        inv_label = inv.invoice_number or "-"
        for item in inv.line_items:
            item_rows.append(
                {
                    "Invoice #": inv_label,
                    "Description": item.description,
                    "Qty": item.quantity,
                    "Unit Price": f"{item.unit_price:.2f}" if item.unit_price else "-",
                    "Amount": f"{item.amount:.2f}" if item.amount else "-",
                }
            )
    cols = ["Invoice #", "Description", "Qty", "Unit Price", "Amount"]
    items_df = pd.DataFrame(item_rows, columns=cols) if item_rows else pd.DataFrame(columns=cols)

    validation_parts = list(error_messages)
    for inv in invoices:
        label = inv.invoice_number or Path(inv.source_file).name if inv.source_file else "Unknown"
        if inv.is_valid:
            validation_parts.append(f"{label}: [OK] Valid")
        else:
            msgs = "; ".join(inv.validation_errors)
            validation_parts.append(f"{label}: [ISSUES] {msgs}")
    validation_text = "\n".join(validation_parts) if validation_parts else "No validation issues."

    raw_text = invoices[0].raw_text or "" if invoices else ""

    return summary_df, items_df, validation_text, raw_text, invoices


def export_files(invoices, fmt):
    if not invoices:
        return None

    suffix_map = {"csv": ".csv", "json": ".json", "excel": ".xlsx"}
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix_map[fmt])
    tmp_path = tmp.name
    tmp.close()

    exporters = {
        "csv": CSVExporter,
        "json": JSONExporter,
        "excel": ExcelExporter,
    }

    exporter = exporters[fmt]()
    exporter.export(invoices, tmp_path)
    return tmp_path


def clear_all():
    return (
        pd.DataFrame(),
        pd.DataFrame(),
        "",
        "",
        [],
        None,
        None,
        None,
        None,
    )


def build_app():
    with gr.Blocks(title="InvoiceXtract") as demo:
        gr.Markdown("""
            # InvoiceXtract
            Upload invoice PDFs or images to automatically extract structured data.
            """)

        invoice_state = gr.State([])

        with gr.Row():
            file_input = gr.File(
                label="Upload Invoice(s)",
                file_count="multiple",
                file_types=[".pdf", ".png", ".jpg", ".jpeg", ".tiff"],
            )

        with gr.Row():
            extract_btn = gr.Button("Extract Data", variant="primary")
            clear_btn = gr.Button("Clear")

        with gr.Tabs():
            with gr.TabItem("Summary"):
                summary_output = gr.Dataframe(
                    label="Invoice Summary",
                    interactive=False,
                )
            with gr.TabItem("Line Items"):
                items_output = gr.Dataframe(
                    label="Line Items",
                    interactive=False,
                )
            with gr.TabItem("Validation"):
                validation_output = gr.Textbox(
                    label="Validation Messages",
                    lines=5,
                    interactive=False,
                )
            with gr.TabItem("Raw Text"):
                raw_text_output = gr.Textbox(
                    label="Extracted Raw Text",
                    lines=15,
                    interactive=False,
                )

        gr.Markdown("### Export Results")
        with gr.Row():
            csv_btn = gr.Button("Download CSV")
            json_btn = gr.Button("Download JSON")
            excel_btn = gr.Button("Download Excel")

        csv_file = gr.File(visible=False)
        json_file = gr.File(visible=False)
        excel_file = gr.File(visible=False)

        extract_btn.click(
            fn=process_files,
            inputs=file_input,
            outputs=[
                summary_output,
                items_output,
                validation_output,
                raw_text_output,
                invoice_state,
            ],
        )

        clear_btn.click(
            fn=clear_all,
            inputs=[],
            outputs=[
                summary_output,
                items_output,
                validation_output,
                raw_text_output,
                invoice_state,
                csv_file,
                json_file,
                excel_file,
                file_input,
            ],
        )

        csv_btn.click(
            fn=export_files,
            inputs=[invoice_state, gr.State("csv")],
            outputs=csv_file,
        )

        json_btn.click(
            fn=export_files,
            inputs=[invoice_state, gr.State("json")],
            outputs=json_file,
        )

        excel_btn.click(
            fn=export_files,
            inputs=[invoice_state, gr.State("excel")],
            outputs=excel_file,
        )

    return demo


def main():
    app = build_app()
    app.launch(show_error=True)


if __name__ == "__main__":
    main()
