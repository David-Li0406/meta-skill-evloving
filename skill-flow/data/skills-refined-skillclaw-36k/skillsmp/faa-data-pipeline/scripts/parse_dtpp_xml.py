#!/usr/bin/env python3
"""
Parse FAA d-TPP (Digital Terminal Procedures Publication) XML metafile.

The d-TPP_Metafile.xml contains metadata about all approach plates,
airport diagrams, and other terminal procedures charts.

Usage:
    python parse_dtpp_xml.py --input d-TPP_Metafile.xml --output aviation.db
"""

import argparse
import sqlite3
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional


def create_charts_table(conn: sqlite3.Connection):
    """Create the charts table for d-TPP metadata."""
    conn.execute('''
        CREATE TABLE IF NOT EXISTS charts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state_code TEXT,
            state_name TEXT,
            city_name TEXT,
            airport_id TEXT,
            airport_name TEXT,
            chart_seq TEXT,
            chart_code TEXT,
            chart_name TEXT,
            user_action TEXT,
            pdf_name TEXT,
            cn_flag TEXT,
            cn_page TEXT,
            cn_date TEXT,
            bvsection TEXT,
            procedure_uid TEXT,
            two_colored TEXT,
            civil TEXT,
            military TEXT,
            copter TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(airport_id, chart_code, chart_name)
        )
    ''')

    conn.execute('CREATE INDEX IF NOT EXISTS idx_charts_airport ON charts(airport_id)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_charts_code ON charts(chart_code)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_charts_state ON charts(state_code)')

    conn.commit()


# Chart code descriptions
CHART_CODES = {
    'APD': 'Airport Diagram',
    'MIN': 'Takeoff Minimums',
    'STAR': 'Standard Terminal Arrival',
    'IAP': 'Instrument Approach Procedure',
    'DP': 'Departure Procedure',
    'ODP': 'Obstacle Departure Procedure',
    'LAH': 'LAHSO',
    'HOT': 'Hot Spot',
    'DAU': 'Diverse Vector Area',
}


def parse_dtpp_xml(xml_path: Path, conn: sqlite3.Connection, verbose: bool = False) -> tuple[int, int]:
    """
    Parse d-TPP XML metafile and insert records.

    Returns:
        tuple: (records_inserted, errors)
    """
    count = 0
    errors = 0

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return 0, 1

    # Navigate the XML structure
    # Structure: digital_tpp -> state_code -> city_name -> airport_name -> record
    for state in root.findall('.//state_code'):
        state_code = state.get('ID', '')
        state_name = state.get('state_fullname', '')

        for city in state.findall('city_name'):
            city_name = city.get('ID', '')

            for airport in city.findall('airport_name'):
                airport_id = airport.get('apt_ident', '')
                airport_name = airport.get('ID', '')
                military = airport.get('military', '')

                for record in airport.findall('record'):
                    try:
                        chart_data = {
                            'state_code': state_code,
                            'state_name': state_name,
                            'city_name': city_name,
                            'airport_id': airport_id,
                            'airport_name': airport_name,
                            'chart_seq': record.findtext('chartseq', ''),
                            'chart_code': record.findtext('chart_code', ''),
                            'chart_name': record.findtext('chart_name', ''),
                            'user_action': record.findtext('useraction', ''),
                            'pdf_name': record.findtext('pdf_name', ''),
                            'cn_flag': record.findtext('cn_flg', ''),
                            'cn_page': record.findtext('cnpage', ''),
                            'cn_date': record.findtext('cndate', ''),
                            'bvsection': record.findtext('bvsection', ''),
                            'procedure_uid': record.findtext('procuid', ''),
                            'two_colored': record.findtext('two_colored', ''),
                            'civil': record.findtext('civil', ''),
                            'military': military,
                            'copter': record.findtext('copession', ''),
                        }

                        conn.execute('''
                            INSERT OR REPLACE INTO charts (
                                state_code, state_name, city_name, airport_id, airport_name,
                                chart_seq, chart_code, chart_name, user_action, pdf_name,
                                cn_flag, cn_page, cn_date, bvsection, procedure_uid,
                                two_colored, civil, military, copter
                            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                        ''', (
                            chart_data['state_code'],
                            chart_data['state_name'],
                            chart_data['city_name'],
                            chart_data['airport_id'],
                            chart_data['airport_name'],
                            chart_data['chart_seq'],
                            chart_data['chart_code'],
                            chart_data['chart_name'],
                            chart_data['user_action'],
                            chart_data['pdf_name'],
                            chart_data['cn_flag'],
                            chart_data['cn_page'],
                            chart_data['cn_date'],
                            chart_data['bvsection'],
                            chart_data['procedure_uid'],
                            chart_data['two_colored'],
                            chart_data['civil'],
                            chart_data['military'],
                            chart_data['copter']
                        ))

                        count += 1
                        if verbose and count % 5000 == 0:
                            print(f"  Processed {count} charts...")

                    except (sqlite3.Error, AttributeError) as e:
                        errors += 1
                        if verbose:
                            print(f"  Error: {e}")

    return count, errors


def main():
    parser = argparse.ArgumentParser(description='Parse FAA d-TPP XML metafile')
    parser.add_argument('--input', '-i', required=True, help='Path to d-TPP_Metafile.xml')
    parser.add_argument('--output', '-o', required=True, help='Path to SQLite database')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {input_path} not found")
        sys.exit(1)

    conn = sqlite3.connect(args.output)
    create_charts_table(conn)

    print(f"Parsing {input_path}...")
    count, errors = parse_dtpp_xml(input_path, conn, args.verbose)

    conn.commit()

    # Get chart type statistics
    cursor = conn.execute('''
        SELECT chart_code, COUNT(*) as cnt
        FROM charts
        GROUP BY chart_code
        ORDER BY cnt DESC
    ''')
    print("\nChart types:")
    for row in cursor.fetchall():
        code = row[0]
        desc = CHART_CODES.get(code, code)
        print(f"  {code}: {row[1]} ({desc})")

    conn.close()

    print(f"\nComplete: {count} charts, {errors} errors")


if __name__ == '__main__':
    main()
