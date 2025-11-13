#!/usr/bin/env python3
"""
Flask Web Application for Stock Comparison Tool
Provides a drag-and-drop interface for comparing stock lists.
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import pandas as pd
from stock_comparison_tool import StockComparator
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_top10_pdf(comparator, output_path, summary):
    """Generate a PDF with Top 10 Price & Quantity Movers - Apple-inspired design."""
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                           rightMargin=0.6*inch, leftMargin=0.6*inch,
                           topMargin=0.5*inch, bottomMargin=0.6*inch)

    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1d1d1f'),
        spaceAfter=8,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=16,
        textColor=colors.HexColor('#1d1d1f'),
        fontName='Helvetica-Bold',
        spaceAfter=6,
        alignment=TA_CENTER
    )

    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#1d1d1f'),
        spaceAfter=12,
        spaceBefore=6,
        fontName='Helvetica-Bold'
    )

    item_style = ParagraphStyle(
        'ItemName',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#1d1d1f'),
        fontName='Helvetica-Bold',
        spaceAfter=4,
        keepWithNext=True  # Prevent orphaning
    )

    detail_style = ParagraphStyle(
        'Detail',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#1d1d1f'),  # Darker text for better readability
        fontName='Helvetica',
        leftIndent=12,
        spaceAfter=2,
        keepWithNext=True  # Keep detail lines together
    )

    # Title - Only "Stock Comparison Report"
    story.append(Paragraph("Stock Comparison Report", subtitle_style))

    # Timestamp with black text
    timestamp_style = ParagraphStyle('Timestamp', parent=styles['Normal'],
                                    fontSize=9, textColor=colors.HexColor('#1d1d1f'), alignment=TA_CENTER)
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", timestamp_style))
    story.append(Spacer(1, 0.25*inch))

    # Helper function to format item name
    def format_item_name(row):
        parts = [str(row['Model'])]
        if pd.notna(row['Capacity']) and row['Capacity']:
            parts.append(str(row['Capacity']))
        if pd.notna(row['Lock Status']) and row['Lock Status']:
            parts.append(f"({row['Lock Status']})")
        if pd.notna(row['Grade']) and row['Grade']:
            parts.append(f"(DLS {row['Grade']})")
        return ' '.join(parts)

    # Get Top 20 data
    if len(comparator.df_filtered) > 0:
        # Top 20 Price Increases
        price_increases = comparator.df_filtered[comparator.df_filtered['List Price Change %'] > 0].nlargest(20, 'List Price Change %')

        # Top 20 Price Decreases
        price_decreases = comparator.df_filtered[comparator.df_filtered['List Price Change %'] < 0].nsmallest(20, 'List Price Change %')

        # Top 20 Quantity Increases
        qty_increases = comparator.df_filtered[comparator.df_filtered['Qty Change'] > 0].nlargest(20, 'Qty Change')

        # Top 20 Quantity Decreases
        qty_decreases = comparator.df_filtered[comparator.df_filtered['Qty Change'] < 0].nsmallest(20, 'Qty Change')

        # Section 1: Top 20 Price Increases
        story.append(Paragraph("1. TOP 20 PRICE INCREASES (with qty change ≥ 100)", section_style))
        story.append(Spacer(1, 0.1*inch))

        if len(price_increases) > 0:
            for idx, row in price_increases.iterrows():
                # Create item group to keep together
                item_group = []

                # Item name
                item_name = format_item_name(row)
                item_group.append(Paragraph(item_name, item_style))

                # Price details with color-coded percentage
                price_pct = row['List Price Change %']
                price_color = '#059669' if price_pct > 0 else '#dc2626' if price_pct < 0 else '#1d1d1f'
                price_detail = f"Price: ${row['OLD List Price']:.2f} → ${row['NEW List Price']:.2f} | Change: ${row['List Price Change $']:+.2f} (<font color='{price_color}'><b>{price_pct:+.1f}%</b></font>)"
                item_group.append(Paragraph(price_detail, detail_style))

                # Quantity details with color-coded percentage
                qty_pct = row['Qty Change %']
                qty_color = '#059669' if qty_pct > 0 else '#dc2626' if qty_pct < 0 else '#1d1d1f'
                qty_detail = f"QTY: {int(row['OLD Qty']):,} → {int(row['NEW Qty']):,} | Change: {int(row['Qty Change']):+,} (<font color='{qty_color}'><b>{qty_pct:+.1f}%</b></font>)"
                item_group.append(Paragraph(qty_detail, detail_style))

                # Keep item together on same page
                story.append(KeepTogether(item_group))
                story.append(Spacer(1, 0.08*inch))
        else:
            story.append(Paragraph("No price increases found with qty change ≥ 100", detail_style))

        story.append(PageBreak())

        # Section 2: Top 10 Price Decreases
        story.append(Paragraph("2. TOP 20 PRICE DECREASES (with qty change ≥ 100)", section_style))
        story.append(Spacer(1, 0.1*inch))

        if len(price_decreases) > 0:
            for idx, row in price_decreases.iterrows():
                # Create item group to keep together
                item_group = []

                # Item name
                item_name = format_item_name(row)
                item_group.append(Paragraph(item_name, item_style))

                # Price details with color-coded percentage
                price_pct = row['List Price Change %']
                price_color = '#059669' if price_pct > 0 else '#dc2626' if price_pct < 0 else '#1d1d1f'
                price_detail = f"Price: ${row['OLD List Price']:.2f} → ${row['NEW List Price']:.2f} | Change: ${row['List Price Change $']:+.2f} (<font color='{price_color}'><b>{price_pct:+.1f}%</b></font>)"
                item_group.append(Paragraph(price_detail, detail_style))

                # Quantity details with color-coded percentage
                qty_pct = row['Qty Change %']
                qty_color = '#059669' if qty_pct > 0 else '#dc2626' if qty_pct < 0 else '#1d1d1f'
                qty_detail = f"QTY: {int(row['OLD Qty']):,} → {int(row['NEW Qty']):,} | Change: {int(row['Qty Change']):+,} (<font color='{qty_color}'><b>{qty_pct:+.1f}%</b></font>)"
                item_group.append(Paragraph(qty_detail, detail_style))

                # Keep item together on same page
                story.append(KeepTogether(item_group))
                story.append(Spacer(1, 0.08*inch))
        else:
            story.append(Paragraph("No price decreases found with qty change ≥ 100", detail_style))

        story.append(PageBreak())

        # Section 3: Top 10 Quantity Increases
        story.append(Paragraph("3. TOP 20 QUANTITY INCREASES (with qty change ≥ 100)", section_style))
        story.append(Spacer(1, 0.1*inch))

        if len(qty_increases) > 0:
            for idx, row in qty_increases.iterrows():
                # Create item group to keep together
                item_group = []

                # Item name
                item_name = format_item_name(row)
                item_group.append(Paragraph(item_name, item_style))

                # Quantity details (primary metric for this section) with color-coded percentage
                qty_pct = row['Qty Change %']
                qty_color = '#059669' if qty_pct > 0 else '#dc2626' if qty_pct < 0 else '#1d1d1f'
                qty_detail = f"QTY: {int(row['OLD Qty']):,} → {int(row['NEW Qty']):,} units | Change: {int(row['Qty Change']):+,} (<font color='{qty_color}'><b>{qty_pct:+.1f}%</b></font>)"
                item_group.append(Paragraph(qty_detail, detail_style))

                # Price details (secondary context) with color-coded percentage
                price_pct = row['List Price Change %']
                price_color = '#059669' if price_pct > 0 else '#dc2626' if price_pct < 0 else '#1d1d1f'
                price_detail = f"PRICE: ${row['OLD List Price']:.2f} → ${row['NEW List Price']:.2f} | Change: ${row['List Price Change $']:+.2f} (<font color='{price_color}'><b>{price_pct:+.1f}%</b></font>)"
                item_group.append(Paragraph(price_detail, detail_style))

                # Keep item together on same page
                story.append(KeepTogether(item_group))
                story.append(Spacer(1, 0.08*inch))
        else:
            story.append(Paragraph("No quantity increases found with qty change ≥ 100", detail_style))

        story.append(PageBreak())

        # Section 4: Top 10 Quantity Decreases
        story.append(Paragraph("4. TOP 20 QUANTITY DECREASES (with qty change ≥ 100)", section_style))
        story.append(Spacer(1, 0.1*inch))

        if len(qty_decreases) > 0:
            for idx, row in qty_decreases.iterrows():
                # Create item group to keep together
                item_group = []

                # Item name
                item_name = format_item_name(row)
                item_group.append(Paragraph(item_name, item_style))

                # Quantity details (primary metric for this section) with color-coded percentage
                qty_pct = row['Qty Change %']
                qty_color = '#059669' if qty_pct > 0 else '#dc2626' if qty_pct < 0 else '#1d1d1f'
                qty_detail = f"QTY: {int(row['OLD Qty']):,} → {int(row['NEW Qty']):,} units | Change: {int(row['Qty Change']):+,} (<font color='{qty_color}'><b>{qty_pct:+.1f}%</b></font>)"
                item_group.append(Paragraph(qty_detail, detail_style))

                # Price details (secondary context) with color-coded percentage
                price_pct = row['List Price Change %']
                price_color = '#059669' if price_pct > 0 else '#dc2626' if price_pct < 0 else '#1d1d1f'
                price_detail = f"PRICE: ${row['OLD List Price']:.2f} → ${row['NEW List Price']:.2f} | Change: ${row['List Price Change $']:+.2f} (<font color='{price_color}'><b>{price_pct:+.1f}%</b></font>)"
                item_group.append(Paragraph(price_detail, detail_style))

                # Keep item together on same page
                story.append(KeepTogether(item_group))
                story.append(Spacer(1, 0.08*inch))
        else:
            story.append(Paragraph("No quantity decreases found with qty change ≥ 100", detail_style))

    else:
        story.append(Paragraph("No significant changes detected.", detail_style))

    # Footer
    story.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'],
                                  fontSize=8, textColor=colors.HexColor('#86868b'), alignment=TA_CENTER)
    story.append(Paragraph("For full detailed analysis, please refer to the Excel workbook or Text report.", footer_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("HYLA Stock Comparison Tool", footer_style))

    # Build PDF
    doc.build(story)
    return output_path


def generate_pdf_report(comparator, output_path, summary):
    """Generate a PDF report from comparison results."""
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=1*inch, bottomMargin=1*inch)

    story = []
    styles = getSampleStyleSheet()

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    story.append(Paragraph("HYLA Stock Comparison Report", title_style))
    story.append(Spacer(1, 0.2*inch))

    # Timestamp
    timestamp_style = ParagraphStyle('Timestamp', parent=styles['Normal'],
                                    fontSize=10, textColor=colors.grey, alignment=TA_CENTER)
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", timestamp_style))
    story.append(Spacer(1, 0.3*inch))

    # Summary Statistics
    story.append(Paragraph("Executive Summary", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))

    summary_data = [
        ['Metric', 'Value'],
        ['Total Configurations (OLD)', f"{summary['total_configs_old']:,}"],
        ['Total Configurations (NEW)', f"{summary['total_configs_new']:,}"],
        ['Matching Configurations', f"{summary['matching_configs']:,}"],
        ['New Configurations', f"{summary['new_configs']:,}"],
        ['Removed Configurations', f"{summary['removed_configs']:,}"],
        ['Significant Changes', f"{summary['significant_changes']:,}"],
        ['Net Quantity Change', f"{summary['net_qty_change']:+,.0f}"],
        ['Avg Price (OLD)', f"${summary['avg_price_old']:.2f}"],
        ['Avg Price (NEW)', f"${summary['avg_price_new']:.2f}"],
    ]

    summary_table = Table(summary_data, colWidths=[3.5*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.3*inch))

    # Top Changes Section
    story.append(Paragraph("Significant Changes", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))

    if len(comparator.df_filtered) > 0:
        # Get top 10 changes
        top_changes = comparator.df_filtered.head(10)

        changes_data = [['Model', 'Carrier', 'Storage', 'Qty Change', 'Price Change']]

        for _, row in top_changes.iterrows():
            changes_data.append([
                str(row.get('Model', 'N/A'))[:20],
                str(row.get('Carrier', 'N/A'))[:15],
                str(row.get('Storage', 'N/A'))[:10],
                f"{row.get('Qty Change', 0):+,.0f}",
                f"${row.get('List Price Change', 0):+,.2f}"
            ])

        changes_table = Table(changes_data, colWidths=[1.5*inch, 1.2*inch, 1*inch, 1*inch, 1*inch])
        changes_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        story.append(changes_table)
    else:
        story.append(Paragraph("No significant changes detected.", styles['Normal']))

    story.append(Spacer(1, 0.3*inch))

    # Footer
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'],
                                  fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("For detailed analysis, please refer to the Excel workbook.", footer_style))
    story.append(Paragraph("HYLA Stock Comparison Tool - Powered by AI", footer_style))

    # Build PDF
    doc.build(story)
    return output_path


@app.route('/')
def index():
    """Serve the main dashboard page."""
    return render_template('index.html')


@app.route('/api/compare', methods=['POST'])
def compare_files():
    """Handle file upload and comparison."""
    try:
        # Validate files
        if 'old_file' not in request.files or 'new_file' not in request.files:
            return jsonify({'error': 'Both OLD and NEW files are required'}), 400

        old_file = request.files['old_file']
        new_file = request.files['new_file']

        if old_file.filename == '' or new_file.filename == '':
            return jsonify({'error': 'No files selected'}), 400

        if not (allowed_file(old_file.filename) and allowed_file(new_file.filename)):
            return jsonify({'error': 'Only Excel files (.xlsx, .xls) are allowed'}), 400

        # Save uploaded files
        old_filename = secure_filename(old_file.filename)
        new_filename = secure_filename(new_file.filename)

        old_path = os.path.join(app.config['UPLOAD_FOLDER'], old_filename)
        new_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

        old_file.save(old_path)
        new_file.save(new_path)

        # Generate output filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(app.config['UPLOAD_FOLDER'], f'Comparison_{timestamp}.txt')

        # Run comparison
        comparator = StockComparator(old_path, new_path, output_file)
        success = comparator.run()

        if not success:
            return jsonify({'error': 'Comparison failed. Please check your files.'}), 500

        # Generate summary statistics first (needed for PDF)
        matching = comparator.df_comparison[comparator.df_comparison['Status'] == 'Matching']
        summary = {
            'total_configs_old': int(len(comparator.df_old_grouped)),
            'total_configs_new': int(len(comparator.df_new_grouped)),
            'matching_configs': int(len(matching)),
            'removed_configs': int((comparator.df_comparison['Status'] == 'Removed').sum()),
            'new_configs': int((comparator.df_comparison['Status'] == 'New').sum()),
            'significant_changes': int(len(comparator.df_filtered)),
            'net_qty_change': float(matching['Qty Change'].sum()) if len(matching) > 0 else 0.0,
            'avg_price_old': float(matching[matching['OLD List Price'] > 0]['OLD List Price'].mean()) if len(matching) > 0 else 0.0,
            'avg_price_new': float(matching[matching['NEW List Price'] > 0]['NEW List Price'].mean()) if len(matching) > 0 else 0.0,
            'timestamp': timestamp
        }

        # Generate Top 20 Movers PDF
        pdf_file = comparator.text_file.replace('.txt', '_Top10.pdf')
        generate_top10_pdf(comparator, pdf_file, summary)

        # Read text report content for inline display
        text_content = ""
        if os.path.exists(comparator.text_file):
            with open(comparator.text_file, 'r', encoding='utf-8') as f:
                text_content = f.read()

        # Store result paths in session/temp
        session_id = timestamp

        return jsonify({
            'success': True,
            'summary': summary,
            'session_id': session_id,
            'text_content': text_content,  # Include text content for inline display
            'files': {
                'pdf': f'/api/download/{session_id}/pdf',
                'excel': f'/api/download/{session_id}/excel',
                'html': f'/api/download/{session_id}/html',
                'zip': f'/api/download/{session_id}/zip',
                'text': f'/api/download/{session_id}/text'
            }
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Error processing files: {str(e)}'}), 500


@app.route('/api/download/<session_id>/<file_type>')
def download_file(session_id, file_type):
    """Download result files."""
    try:
        # Find files with matching session_id (timestamp)
        files = list(Path(app.config['UPLOAD_FOLDER']).glob(f'*{session_id}*'))

        if file_type == 'pdf':
            file_path = next((f for f in files if f.suffix == '.pdf'), None)
        elif file_type == 'excel':
            file_path = next((f for f in files if f.suffix == '.xlsx'), None)
        elif file_type == 'html':
            file_path = next((f for f in files if f.suffix == '.html'), None)
        elif file_type == 'zip':
            file_path = next((f for f in files if f.suffix == '.zip'), None)
        elif file_type == 'text':
            file_path = next((f for f in files if f.suffix == '.txt'), None)
        else:
            return jsonify({'error': 'Invalid file type'}), 400

        if not file_path or not file_path.exists():
            return jsonify({'error': 'File not found'}), 404

        # CRITICAL: Force download by using octet-stream and proper headers
        download_name = file_path.name

        # Read file into memory to ensure we control the response
        with open(file_path, 'rb') as f:
            file_data = f.read()

        from flask import make_response
        response = make_response(file_data)
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = f'attachment; filename="{download_name}"'
        response.headers['Content-Length'] = len(file_data)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['X-Content-Type-Options'] = 'nosniff'

        return response

    except Exception as e:
        return jsonify({'error': f'Error downloading file: {str(e)}'}), 500


@app.route('/api/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


# Cleanup old files on startup
def cleanup_old_files():
    """Clean up old temporary files."""
    try:
        folder = app.config['UPLOAD_FOLDER']
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
    except Exception as e:
        print(f"Error cleaning up files: {e}")


if __name__ == '__main__':
    cleanup_old_files()
    port = int(os.environ.get('PORT', 5001))
    print("=" * 80)
    print("HYLA STOCK COMPARISON DASHBOARD")
    print("=" * 80)
    print(f"Starting server at http://localhost:{port}")
    print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    print("=" * 80)
    app.run(debug=False, host='0.0.0.0', port=port)
