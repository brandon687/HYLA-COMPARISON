#!/usr/bin/env python3
"""
Stock List Comparison Tool
Compares OLD and NEW stock lists to provide purchasing insights.

Usage:
    python stock_comparison_tool.py <old_file.xlsx> <new_file.xlsx> [output_file.txt]
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os
from pathlib import Path
import subprocess
import zipfile


class StockComparator:
    """Compares two stock list Excel files and generates analysis."""

    def __init__(self, old_file, new_file, output_file=None):
        self.old_file = old_file
        self.new_file = new_file
        self.output_file = output_file or f"Stock_Comparison_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        # Determine file format from output_file extension
        if self.output_file.endswith('.xlsx'):
            self.excel_file = self.output_file
            self.text_file = self.output_file.replace('.xlsx', '.txt')
        else:
            self.text_file = self.output_file
            self.excel_file = self.output_file.replace('.txt', '.xlsx')

        self.df_old = None
        self.df_new = None
        self.df_old_grouped = None
        self.df_new_grouped = None
        self.df_comparison = None
        self.df_filtered = None

    def format_item_name(self, row):
        """Create item name from grouping columns."""
        parts = []
        if pd.notna(row['Model']) and row['Model']:
            parts.append(str(row['Model']))
        if pd.notna(row['Capacity']) and row['Capacity']:
            parts.append(str(row['Capacity']))
        if pd.notna(row['Color']) and row['Color']:
            parts.append(str(row['Color']))
        if pd.notna(row['Lock Status']) and row['Lock Status']:
            parts.append(f"({row['Lock Status']})")
        if pd.notna(row['Grade']) and row['Grade']:
            parts.append(f"(DLS {row['Grade']})")
        return ' '.join(parts) if parts else "Unknown Item"

    def load_data(self):
        """Load and prepare data from both files."""
        print("Loading data...")

        # Load OLD file (detect header row)
        try:
            # Try to find the header row in OLD file
            df_temp = pd.read_excel(self.old_file, header=None, nrows=20)
            header_row = None
            for i in range(len(df_temp)):
                if str(df_temp.iloc[i, 0]).strip() == 'Item #':
                    header_row = i
                    break

            if header_row is None:
                # No header metadata, try default
                self.df_old = pd.read_excel(self.old_file)
            else:
                self.df_old = pd.read_excel(self.old_file, header=header_row)

            print(f"✓ Loaded OLD file: {len(self.df_old)} rows")
        except Exception as e:
            print(f"✗ Error loading OLD file: {e}")
            raise

        # Load NEW file (detect header row)
        try:
            # Try to find the header row
            df_temp = pd.read_excel(self.new_file, header=None, nrows=20)
            header_row = None
            for i in range(len(df_temp)):
                if str(df_temp.iloc[i, 0]).strip() == 'Item #':
                    header_row = i
                    break

            if header_row is None:
                # No header metadata, try default
                self.df_new = pd.read_excel(self.new_file)
            else:
                self.df_new = pd.read_excel(self.new_file, header=header_row)

            print(f"✓ Loaded NEW file: {len(self.df_new)} rows")
        except Exception as e:
            print(f"✗ Error loading NEW file: {e}")
            raise

    def clean_data(self):
        """Clean and prepare data for comparison."""
        print("\nCleaning data...")

        # Validate required columns
        required_cols = ['Item #', 'Model', 'Capacity', 'Color', 'Lock Status', 'Grade',
                        'Available Quantity', 'List Price']

        for col in required_cols:
            if col not in self.df_old.columns:
                raise ValueError(f"Required column '{col}' not found in OLD file")
            if col not in self.df_new.columns:
                raise ValueError(f"Required column '{col}' not found in NEW file")

        # Track duplicates but DON'T remove them yet
        # (Colleague's approach: keep all rows for configuration grouping)
        old_dupes = self.df_old.duplicated(subset=['Item #'], keep='first').sum()
        new_dupes = self.df_new.duplicated(subset=['Item #'], keep='first').sum()

        old_unique = self.df_old['Item #'].nunique()
        new_unique = self.df_new['Item #'].nunique()

        print(f"  OLD file: {len(self.df_old)} rows, {old_unique} unique items, {old_dupes} duplicates")
        print(f"  NEW file: {len(self.df_new)} rows, {new_unique} unique items, {new_dupes} duplicates")

        # Convert Item # to string
        self.df_old['Item #'] = self.df_old['Item #'].astype(str)
        self.df_new['Item #'] = self.df_new['Item #'].astype(str)

        # Ensure numeric columns are numeric
        numeric_cols = ['Available Quantity', 'List Price', 'New Offer Price']
        for col in numeric_cols:
            if col in self.df_old.columns:
                self.df_old[col] = pd.to_numeric(self.df_old[col], errors='coerce')
            if col in self.df_new.columns:
                self.df_new[col] = pd.to_numeric(self.df_new[col], errors='coerce')

        print(f"✓ Data cleaned and ready for grouping")

    def group_by_configuration(self):
        """Group items by configuration (Model + Capacity + Color + Lock Status + Grade)."""
        print("\nGrouping by configuration...")

        grouping_cols = ['Model', 'Capacity', 'Color', 'Lock Status', 'Grade']

        # Calculate weighted averages for OLD file
        # Weighted average = sum(price * qty) / sum(qty)
        self.df_old['Weighted_List_Price'] = self.df_old['List Price'] * self.df_old['Available Quantity']
        self.df_old['Weighted_Offer_Price'] = self.df_old['New Offer Price'] * self.df_old['Available Quantity']

        self.df_old_grouped = self.df_old.groupby(grouping_cols).agg({
            'Item #': 'count',
            'Available Quantity': 'sum',
            'Weighted_List_Price': 'sum',
            'Weighted_Offer_Price': 'sum'
        }).reset_index()

        # Calculate weighted averages
        self.df_old_grouped['OLD List Price'] = (
            self.df_old_grouped['Weighted_List_Price'] / self.df_old_grouped['Available Quantity']
        )
        self.df_old_grouped['OLD Offer Price'] = (
            self.df_old_grouped['Weighted_Offer_Price'] / self.df_old_grouped['Available Quantity']
        )

        # Rename and select final columns
        self.df_old_grouped = self.df_old_grouped.rename(columns={
            'Item #': 'OLD Item Count',
            'Available Quantity': 'OLD Qty'
        })
        self.df_old_grouped = self.df_old_grouped[['Model', 'Capacity', 'Color', 'Lock Status', 'Grade',
                                                     'OLD Item Count', 'OLD Qty', 'OLD List Price', 'OLD Offer Price']]

        # Calculate weighted averages for NEW file
        self.df_new['Weighted_List_Price'] = self.df_new['List Price'] * self.df_new['Available Quantity']

        self.df_new_grouped = self.df_new.groupby(grouping_cols).agg({
            'Item #': 'count',
            'Available Quantity': 'sum',
            'Weighted_List_Price': 'sum'
        }).reset_index()

        # Calculate weighted average
        self.df_new_grouped['NEW List Price'] = (
            self.df_new_grouped['Weighted_List_Price'] / self.df_new_grouped['Available Quantity']
        )

        # Rename and select final columns
        self.df_new_grouped = self.df_new_grouped.rename(columns={
            'Item #': 'NEW Item Count',
            'Available Quantity': 'NEW Qty'
        })
        self.df_new_grouped = self.df_new_grouped[['Model', 'Capacity', 'Color', 'Lock Status', 'Grade',
                                                     'NEW Item Count', 'NEW Qty', 'NEW List Price']]

        print(f"✓ OLD configurations: {len(self.df_old_grouped)}")
        print(f"✓ NEW configurations: {len(self.df_new_grouped)}")

    def compare_configurations(self):
        """Compare OLD and NEW configurations."""
        print("\nComparing configurations...")

        # Merge on configuration keys
        self.df_comparison = pd.merge(
            self.df_old_grouped,
            self.df_new_grouped,
            on=['Model', 'Capacity', 'Color', 'Lock Status', 'Grade'],
            how='outer',
            indicator=True
        )

        # Add status column
        self.df_comparison['Status'] = self.df_comparison['_merge'].map({
            'both': 'Matching',
            'left_only': 'Removed',
            'right_only': 'New'
        })
        self.df_comparison = self.df_comparison.drop(columns=['_merge'])

        # Calculate changes (only for matching configurations)
        matching_mask = self.df_comparison['Status'] == 'Matching'

        # Quantity changes
        self.df_comparison.loc[matching_mask, 'Qty Change'] = (
            self.df_comparison['NEW Qty'] - self.df_comparison['OLD Qty']
        )
        self.df_comparison.loc[matching_mask, 'Qty Change %'] = (
            (self.df_comparison['Qty Change'] / self.df_comparison['OLD Qty']) * 100
        )

        # List price changes
        self.df_comparison.loc[matching_mask, 'List Price Change $'] = (
            self.df_comparison['NEW List Price'] - self.df_comparison['OLD List Price']
        )
        self.df_comparison.loc[matching_mask, 'List Price Change %'] = (
            (self.df_comparison['List Price Change $'] / self.df_comparison['OLD List Price']) * 100
        )

        # Offer to List price change (strategic metric)
        self.df_comparison.loc[matching_mask, 'From Offer to List Price Change $'] = (
            self.df_comparison['NEW List Price'] - self.df_comparison['OLD Offer Price']
        )
        self.df_comparison.loc[matching_mask, 'From Offer to List Price Change %'] = (
            (self.df_comparison['From Offer to List Price Change $'] / self.df_comparison['OLD Offer Price']) * 100
        )

        # Reorder columns
        col_order = ['Model', 'Capacity', 'Color', 'Lock Status', 'Grade', 'Status',
                    'OLD Item Count', 'OLD Qty', 'OLD List Price', 'OLD Offer Price',
                    'NEW Item Count', 'NEW Qty', 'NEW List Price',
                    'Qty Change', 'Qty Change %',
                    'List Price Change $', 'List Price Change %',
                    'From Offer to List Price Change $', 'From Offer to List Price Change %']
        self.df_comparison = self.df_comparison[col_order]

        matching = (self.df_comparison['Status'] == 'Matching').sum()
        removed = (self.df_comparison['Status'] == 'Removed').sum()
        new = (self.df_comparison['Status'] == 'New').sum()

        print(f"✓ Matching configurations: {matching}")
        print(f"✓ Removed configurations: {removed}")
        print(f"✓ New configurations: {new}")

        # Filter for absolute qty change >= 100 (matching items only)
        matching_df = self.df_comparison[self.df_comparison['Status'] == 'Matching'].copy()
        self.df_filtered = matching_df[abs(matching_df['Qty Change']) >= 100].copy()
        print(f"✓ Items with qty change >= 100: {len(self.df_filtered)}")

    def _generate_top_insights(self):
        """Generate Top 10 insights for each category (filtered items only)."""
        insights = {}

        # Top 10 Price Increases (from filtered data)
        price_increases = self.df_filtered[self.df_filtered['List Price Change %'] > 0].nlargest(10, 'List Price Change %')
        insights['price_increases'] = price_increases

        # Top 10 Price Decreases (from filtered data)
        price_decreases = self.df_filtered[self.df_filtered['List Price Change %'] < 0].nsmallest(10, 'List Price Change %')
        insights['price_decreases'] = price_decreases

        # Top 10 Quantity Increases (from filtered data, by percentage)
        qty_increases = self.df_filtered[self.df_filtered['Qty Change'] > 0].nlargest(10, 'Qty Change %')
        insights['qty_increases'] = qty_increases

        # Top 10 Quantity Decreases (from filtered data, by percentage)
        qty_decreases = self.df_filtered[self.df_filtered['Qty Change'] < 0].nsmallest(10, 'Qty Change %')
        insights['qty_decreases'] = qty_decreases

        return insights

    def _generate_executive_dashboard(self, top_insights):
        """Generate executive HTML dashboard."""
        html_file = self.text_file.replace('.txt', '_Dashboard.html')

        # Prepare data for JavaScript
        price_increases = []
        price_decreases = []
        qty_increases = []
        qty_decreases = []

        for idx, row in top_insights['price_increases'].iterrows():
            price_increases.append({
                'model': f"{row['Model']} {row['Capacity']} {row['Color']} ({row['Lock Status']})",
                'grade': f"DLS {row['Grade']}" if pd.notna(row['Grade']) else "N/A",
                'oldPrice': float(row['OLD List Price']),
                'newPrice': float(row['NEW List Price']),
                'priceChange': float(row['List Price Change %']),
                'oldQty': int(row['OLD Qty']),
                'newQty': int(row['NEW Qty']),
                'qtyChange': float(row['Qty Change %'])
            })

        for idx, row in top_insights['price_decreases'].iterrows():
            price_decreases.append({
                'model': f"{row['Model']} {row['Capacity']} {row['Color']} ({row['Lock Status']})",
                'grade': f"DLS {row['Grade']}" if pd.notna(row['Grade']) else "N/A",
                'oldPrice': float(row['OLD List Price']),
                'newPrice': float(row['NEW List Price']),
                'priceChange': float(row['List Price Change %']),
                'oldQty': int(row['OLD Qty']),
                'newQty': int(row['NEW Qty']),
                'qtyChange': float(row['Qty Change %'])
            })

        for idx, row in top_insights['qty_increases'].iterrows():
            qty_increases.append({
                'model': f"{row['Model']} {row['Capacity']} {row['Color']} ({row['Lock Status']})",
                'grade': f"DLS {row['Grade']}" if pd.notna(row['Grade']) else "N/A",
                'oldQty': int(row['OLD Qty']),
                'newQty': int(row['NEW Qty']),
                'qtyChange': float(row['Qty Change %']),
                'oldPrice': float(row['OLD List Price']),
                'newPrice': float(row['NEW List Price']),
                'priceChange': float(row['List Price Change %'])
            })

        for idx, row in top_insights['qty_decreases'].iterrows():
            qty_decreases.append({
                'model': f"{row['Model']} {row['Capacity']} {row['Color']} ({row['Lock Status']})",
                'grade': f"DLS {row['Grade']}" if pd.notna(row['Grade']) else "N/A",
                'oldQty': int(row['OLD Qty']),
                'newQty': int(row['NEW Qty']),
                'qtyChange': float(row['Qty Change %']),
                'oldPrice': float(row['OLD List Price']),
                'newPrice': float(row['NEW List Price']),
                'priceChange': float(row['List Price Change %'])
            })

        matching = self.df_comparison[self.df_comparison['Status'] == 'Matching']

        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iPhone Stock Comparison - Executive Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
            background: #f5f5f7;
            color: #1d1d1f;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
        }}

        header {{
            text-align: center;
            margin-bottom: 48px;
            animation: fadeIn 0.6s ease-in;
        }}

        h1 {{
            font-size: 48px;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 12px;
            color: #1d1d1f;
        }}

        .subtitle {{
            font-size: 18px;
            color: #6e6e73;
            font-weight: 400;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 48px;
            animation: fadeIn 0.8s ease-in 0.2s both;
        }}

        .stat-card {{
            background: white;
            padding: 28px;
            border-radius: 16px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s;
        }}

        .stat-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        }}

        .stat-label {{
            font-size: 13px;
            color: #86868b;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 8px;
        }}

        .stat-value {{
            font-size: 36px;
            font-weight: 700;
            color: #1d1d1f;
        }}

        .section {{
            margin-bottom: 48px;
            animation: fadeIn 1s ease-in 0.4s both;
        }}

        .section-title {{
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 24px;
            color: #1d1d1f;
        }}

        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 32px;
            margin-bottom: 48px;
        }}

        .chart-card {{
            background: white;
            padding: 32px;
            border-radius: 16px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        }}

        .chart-title {{
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 24px;
            color: #1d1d1f;
        }}

        table {{
            width: 100%;
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            border-collapse: collapse;
        }}

        th {{
            background: #1d1d1f;
            color: white;
            padding: 16px 20px;
            text-align: left;
            font-weight: 600;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        td {{
            padding: 16px 20px;
            border-bottom: 1px solid #d2d2d7;
            font-size: 15px;
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        tr:hover {{
            background: #f5f5f7;
        }}

        .grade-badge {{
            display: inline-block;
            padding: 4px 10px;
            background: #e8e8ed;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            color: #1d1d1f;
            margin-left: 8px;
        }}

        .positive {{ color: #30d158; font-weight: 600; }}
        .negative {{ color: #ff3b30; font-weight: 600; }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @media print {{
            body {{ background: white; }}
            .stat-card, .chart-card, table {{ box-shadow: none; border: 1px solid #d2d2d7; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>iPhone Stock Comparison</h1>
            <p class="subtitle">Executive Report • {datetime.now().strftime('%B %d, %Y')}</p>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Configs</div>
                <div class="stat-value">{len(self.df_old_grouped)} → {len(self.df_new_grouped)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Matching Items</div>
                <div class="stat-value">{len(matching):,}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Significant Changes</div>
                <div class="stat-value">{len(self.df_filtered)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Net Qty Change</div>
                <div class="stat-value">{matching['Qty Change'].sum():+,.0f}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Price (OLD)</div>
                <div class="stat-value">${matching[matching['OLD List Price'] > 0]['OLD List Price'].mean():.0f}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Price (NEW)</div>
                <div class="stat-value">${matching[matching['NEW List Price'] > 0]['NEW List Price'].mean():.0f}</div>
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">Analysis Complete</h2>
            <p style="text-align: center; color: #6e6e73; font-size: 16px; margin-top: 24px; line-height: 1.6;">
                Your stock comparison has been completed successfully.<br>
                For detailed analysis and full data, please refer to the <strong>Excel workbook</strong> or <strong>Text report</strong>.
            </p>
        </div>
    </div>

    <script>
        // Dashboard loaded successfully
        console.log('HYLA Stock Comparison Dashboard loaded');
    </script>
</body>
</html>'''

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✓ Executive dashboard generated: {html_file}")
        return html_file

    def export_to_excel(self):
        """Export comparison results to Excel workbook."""
        print(f"\nGenerating Excel workbook...")

        try:
            with pd.ExcelWriter(self.excel_file, engine='openpyxl') as writer:
                # Sheet 1: Summary Statistics
                matching = self.df_comparison[self.df_comparison['Status'] == 'Matching']
                summary_data = {
                    'Metric': [
                        'Total Configurations (OLD)',
                        'Total Configurations (NEW)',
                        'Matching Configurations',
                        'Removed Configurations',
                        'New Configurations',
                        'Items with Qty Change >= 100',
                        '',
                        'Total Quantity (OLD)',
                        'Total Quantity (NEW)',
                        'Net Quantity Change',
                        '',
                        'Average Price (OLD)',
                        'Average Price (NEW)',
                        'Average Price Change'
                    ],
                    'Value': [
                        len(self.df_old_grouped),
                        len(self.df_new_grouped),
                        len(matching),
                        (self.df_comparison['Status'] == 'Removed').sum(),
                        (self.df_comparison['Status'] == 'New').sum(),
                        len(self.df_filtered),
                        '',
                        self.df_old_grouped['OLD Qty'].sum(),
                        self.df_new_grouped['NEW Qty'].sum(),
                        matching['Qty Change'].sum() if len(matching) > 0 else 0,
                        '',
                        matching[matching['OLD List Price'] > 0]['OLD List Price'].mean() if len(matching) > 0 else 0,
                        matching[matching['NEW List Price'] > 0]['NEW List Price'].mean() if len(matching) > 0 else 0,
                        (matching[matching['NEW List Price'] > 0]['NEW List Price'].mean() -
                         matching[matching['OLD List Price'] > 0]['OLD List Price'].mean()) if len(matching) > 0 else 0
                    ]
                }
                df_summary = pd.DataFrame(summary_data)
                df_summary.to_excel(writer, sheet_name='Summary', index=False)

                # Sheet 2: Full Comparison (items with qty change >= 100)
                self.df_filtered.to_excel(writer, sheet_name='Significant Changes', index=False)

                # Sheet 3: All Matching Items
                matching.to_excel(writer, sheet_name='All Matching Items', index=False)

                # Sheet 4: Top Insights
                top_insights = self._generate_top_insights()

                # Price Increases
                if len(top_insights['price_increases']) > 0:
                    top_insights['price_increases'].to_excel(writer, sheet_name='Top Price Increases', index=False)

                # Price Decreases
                if len(top_insights['price_decreases']) > 0:
                    top_insights['price_decreases'].to_excel(writer, sheet_name='Top Price Decreases', index=False)

                # Quantity Increases
                if len(top_insights['qty_increases']) > 0:
                    top_insights['qty_increases'].to_excel(writer, sheet_name='Top Qty Increases', index=False)

                # Quantity Decreases
                if len(top_insights['qty_decreases']) > 0:
                    top_insights['qty_decreases'].to_excel(writer, sheet_name='Top Qty Decreases', index=False)

            print(f"✓ Excel workbook saved: {self.excel_file}")
            return self.excel_file
        except Exception as e:
            print(f"✗ Error generating Excel file: {e}")
            import traceback
            traceback.print_exc()
            return None

    def export_results(self):
        """Export comparison results to text report."""
        print(f"\nGenerating comparison report...")

        # Generate Top 10 insights
        top_insights = self._generate_top_insights()

        report_lines = []
        report_lines.append("="*80)
        report_lines.append("STOCK LIST COMPARISON REPORT")
        report_lines.append("="*80)
        report_lines.append(f"\nOld File: {self.old_file}")
        report_lines.append(f"New File: {self.new_file}")
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}")
        report_lines.append("\n" + "="*80)

        # Section 1: Top 10 Price Increases
        report_lines.append("\n1. TOP 10 PRICE INCREASES (with qty change >= 100)")
        report_lines.append("="*80)
        if len(top_insights['price_increases']) > 0:
            for idx, row in top_insights['price_increases'].iterrows():
                item_name = self.format_item_name(row)
                report_lines.append(f"\n{item_name}")
                report_lines.append(f"  Price: ${row['OLD List Price']:.2f} -> ${row['NEW List Price']:.2f} | Change: ${row['List Price Change $']:+.2f} ({row['List Price Change %']:+.1f}%)")
                report_lines.append(f"  QTY: {row['OLD Qty']:,.0f} -> {row['NEW Qty']:,.0f} | Change: {row['Qty Change']:+,.0f} ({row['Qty Change %']:+.1f}%)")
        else:
            report_lines.append("\nNo price increases found with qty change >= 100")

        # Section 2: Top 10 Price Decreases
        report_lines.append("\n\n" + "="*80)
        report_lines.append("2. TOP 10 PRICE DECREASES (with qty change >= 100)")
        report_lines.append("="*80)
        if len(top_insights['price_decreases']) > 0:
            for idx, row in top_insights['price_decreases'].iterrows():
                item_name = self.format_item_name(row)
                report_lines.append(f"\n{item_name}")
                report_lines.append(f"  Price: ${row['OLD List Price']:.2f} -> ${row['NEW List Price']:.2f} | Change: ${row['List Price Change $']:+.2f} ({row['List Price Change %']:+.1f}%)")
                report_lines.append(f"  QTY: {row['OLD Qty']:,.0f} -> {row['NEW Qty']:,.0f} | Change: {row['Qty Change']:+,.0f} ({row['Qty Change %']:+.1f}%)")
        else:
            report_lines.append("\nNo price decreases found with qty change >= 100")

        # Section 3: Top 10 Qty Increases
        report_lines.append("\n\n" + "="*80)
        report_lines.append("3. TOP 10 QUANTITY INCREASES (with qty change >= 100)")
        report_lines.append("="*80)
        if len(top_insights['qty_increases']) > 0:
            for idx, row in top_insights['qty_increases'].iterrows():
                item_name = self.format_item_name(row)
                report_lines.append(f"\n{item_name}")
                report_lines.append(f"  QTY: {row['OLD Qty']:,.0f} -> {row['NEW Qty']:,.0f} units | Change: {row['Qty Change']:+,.0f} ({row['Qty Change %']:+.1f}%)")
                report_lines.append(f"  PRICE: ${row['OLD List Price']:.2f} -> ${row['NEW List Price']:.2f} | Change: ${row['List Price Change $']:+.2f} ({row['List Price Change %']:+.1f}%)")
        else:
            report_lines.append("\nNo quantity increases found with qty change >= 100")

        # Section 4: Top 10 Qty Decreases
        report_lines.append("\n\n" + "="*80)
        report_lines.append("4. TOP 10 QUANTITY DECREASES (with qty change >= 100)")
        report_lines.append("="*80)
        if len(top_insights['qty_decreases']) > 0:
            for idx, row in top_insights['qty_decreases'].iterrows():
                item_name = self.format_item_name(row)
                report_lines.append(f"\n{item_name}")
                report_lines.append(f"  QTY: {row['OLD Qty']:,.0f} -> {row['NEW Qty']:,.0f} units | Change: {row['Qty Change']:+,.0f} ({row['Qty Change %']:+.1f}%)")
                report_lines.append(f"  PRICE: ${row['OLD List Price']:.2f} -> ${row['NEW List Price']:.2f} | Change: ${row['List Price Change $']:+.2f} ({row['List Price Change %']:+.1f}%)")
        else:
            report_lines.append("\nNo quantity decreases found with qty change >= 100")

        # Section 5: Detailed Comparison
        report_lines.append("\n\n" + "="*80)
        report_lines.append("5. DETAILED COMPARISON BY MODEL-CAPACITY-GRADE-LOCK STATUS")
        report_lines.append("="*80)
        report_lines.append("\nAll items with significant changes (qty change >= 100):")
        report_lines.append(f"\nTotal items: {len(self.df_filtered):,}")

        # Sort by absolute qty change for detailed view
        df_filtered_sorted = self.df_filtered.sort_values('Qty Change', ascending=False, key=abs)

        report_lines.append("\n" + "-"*80)
        for idx, row in df_filtered_sorted.head(50).iterrows():  # Show top 50 most significant changes
            item_name = self.format_item_name(row)
            report_lines.append(f"\n{item_name}")
            report_lines.append(f"  Quantity: {row['OLD Qty']:,.0f} -> {row['NEW Qty']:,.0f} | Change: {row['Qty Change']:+,.0f} ({row['Qty Change %']:+.1f}%)")
            report_lines.append(f"  Price: ${row['OLD List Price']:.2f} -> ${row['NEW List Price']:.2f} | Change: ${row['List Price Change $']:+.2f} ({row['List Price Change %']:+.1f}%)")

        # Summary statistics
        matching = self.df_comparison[self.df_comparison['Status'] == 'Matching']
        report_lines.append("\n\n" + "="*80)
        report_lines.append("6. SUMMARY STATISTICS")
        report_lines.append("="*80)
        report_lines.append(f"\nTotal unique items (old file): {len(self.df_old_grouped):,}")
        report_lines.append(f"Total unique items (new file): {len(self.df_new_grouped):,}")
        report_lines.append(f"Items with qty change >= 100: {len(self.df_filtered):,}")
        report_lines.append(f"\nTotal quantity (old): {self.df_old_grouped['OLD Qty'].sum():,.0f} units")
        report_lines.append(f"Total quantity (new): {self.df_new_grouped['NEW Qty'].sum():,.0f} units")
        report_lines.append(f"Net quantity change: {matching['Qty Change'].sum():+,.0f} units")

        # Price statistics
        valid_old_prices = matching[matching['OLD List Price'] > 0]['OLD List Price']
        valid_new_prices = matching[matching['NEW List Price'] > 0]['NEW List Price']
        if len(valid_old_prices) > 0 and len(valid_new_prices) > 0:
            report_lines.append(f"\nAverage price (old): ${valid_old_prices.mean():.2f}")
            report_lines.append(f"Average price (new): ${valid_new_prices.mean():.2f}")

        report_lines.append("\n" + "="*80)
        report_lines.append("END OF REPORT")
        report_lines.append("="*80)

        # Write report to file
        try:
            with open(self.text_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report_lines))
            print(f"✓ Report saved to: {self.text_file}")
        except Exception as e:
            print(f"✗ ERROR saving report: {e}")
            return None

        print(f"\nReport location: {os.path.abspath(self.text_file)}")
        print(f"Total items analyzed: {len(self.df_comparison):,}")
        print(f"Items with significant changes: {len(self.df_filtered):,}")

        # Generate Excel workbook
        excel_file = self.export_to_excel()
        if excel_file is None:
            return None

        # Generate executive dashboard
        html_file = self._generate_executive_dashboard(top_insights)

        # Create zip package (excluding HTML dashboard)
        zip_file = self.text_file.replace('.txt', '_Package.zip')
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(self.text_file, os.path.basename(self.text_file))
            zipf.write(excel_file, os.path.basename(excel_file))
            # HTML dashboard excluded from package

        print(f"✓ Package created: {zip_file}")

        # Auto-open the Excel file and dashboard
        try:
            subprocess.run(['open', excel_file], check=False)
            subprocess.run(['open', html_file], check=False)
            print(f"✓ Opened Excel workbook and dashboard")
        except Exception as e:
            print(f"⚠ Could not auto-open files: {e}")

        return zip_file

    def run(self):
        """Execute the complete comparison workflow."""
        print("=" * 80)
        print("STOCK LIST COMPARISON TOOL")
        print("=" * 80)
        print(f"OLD file: {self.old_file}")
        print(f"NEW file: {self.new_file}")
        print(f"Output:   {self.excel_file}")
        print("=" * 80)

        try:
            self.load_data()
            self.clean_data()
            self.group_by_configuration()
            self.compare_configurations()
            zip_file = self.export_results()

            print("\n" + "=" * 80)
            print("COMPARISON COMPLETE!")
            print("=" * 80)
            print(f"\n📦 Package: {zip_file}")
            print(f"   Contains: Excel Workbook + Text Report + Executive Dashboard")
            print(f"\nFiles generated:")
            print(f"   • {self.excel_file}")
            print(f"   • {self.text_file}")
            print(f"   • {self.text_file.replace('.txt', '_Dashboard.html')}")
            print(f"   • {zip_file}")

            return True
        except Exception as e:
            print(f"\n✗ Error during comparison: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python stock_comparison_tool.py <old_file.xlsx> <new_file.xlsx> [output_file.txt]")
        print("\nExample:")
        print('  python stock_comparison_tool.py "**OLD**Stock_List.xlsx" "**NEW**Stock_List.xlsx"')
        sys.exit(1)

    old_file = sys.argv[1]
    new_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else None

    # Validate input files exist
    if not os.path.exists(old_file):
        print(f"✗ Error: OLD file not found: {old_file}")
        sys.exit(1)
    if not os.path.exists(new_file):
        print(f"✗ Error: NEW file not found: {new_file}")
        sys.exit(1)

    # Run comparison
    comparator = StockComparator(old_file, new_file, output_file)
    success = comparator.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
