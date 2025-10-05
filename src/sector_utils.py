"""
Sector and industry utilities for company analysis using SIC codes.

Provides functions to map between CIKs, SIC codes, and industry classifications
using data from the knowledge/ directory CSV files.
"""

import pandas as pd
from pathlib import Path
from typing import List, Optional, Dict
import os

# Cache for loaded data to avoid repeated file reads
_companies_df: Optional[pd.DataFrame] = None
_industries_df: Optional[pd.DataFrame] = None


def _get_data_path() -> Path:
    """Get the path to the knowledge directory."""
    current_dir = Path(__file__).parent
    return current_dir.parent / "knowledge"


def _load_companies_data() -> pd.DataFrame:
    """Load and cache companies info CSV data."""
    global _companies_df
    if _companies_df is None:
        data_path = _get_data_path() / "companies_info.csv"
        _companies_df = pd.read_csv(data_path)
        # Ensure cik_str is treated as integer for consistent lookups
        _companies_df['cik_str'] = _companies_df['cik_str'].astype(int)
        # Handle missing industry values (NaN) by filtering them out
        _companies_df = _companies_df.dropna(subset=['industry'])
        _companies_df['industry'] = _companies_df['industry'].astype(int)
    return _companies_df


def _load_industries_data() -> pd.DataFrame:
    """Load and cache SIC industry codes CSV data."""
    global _industries_df
    if _industries_df is None:
        data_path = _get_data_path() / "sic_industry_code.csv"
        _industries_df = pd.read_csv(data_path)
        # Clean up the column name that might have BOM
        _industries_df.columns = _industries_df.columns.str.strip().str.replace('\ufeff', '')
        _industries_df['SIC Code'] = _industries_df['SIC Code'].astype(int)
    return _industries_df


def get_sector_ciks(sector_id: int) -> List[int]:
    """
    Get list of CIKs for companies in a specific SIC sector.

    Args:
        sector_id: SIC industry code (e.g., 3571 for electronic computers)

    Returns:
        List of CIK integers for companies in the sector, sorted

    Raises:
        ValueError: If sector_id is not found in the SIC codes

    Example:
        >>> ciks = get_sector_ciks(3571)  # Electronic computers
        >>> print(ciks)
        [320193, ...]  # Apple and other computer companies
    """
    companies_df = _load_companies_data()
    industries_df = _load_industries_data()

    # Verify sector_id exists
    if sector_id not in industries_df['SIC Code'].values:
        available_codes = sorted(industries_df['SIC Code'].unique())
        raise ValueError(f"Sector ID {sector_id} not found. Available SIC codes: {available_codes[:10]}...")

    # Filter companies by sector
    sector_companies = companies_df[companies_df['industry'] == sector_id]

    # Return sorted list of CIKs
    return sorted(sector_companies['cik_str'].tolist())


def get_cik_sector(cik: int) -> Optional[int]:
    """
    Get the SIC sector code for a specific company CIK.

    Args:
        cik: Company CIK identifier

    Returns:
        SIC sector code, or None if CIK not found

    Example:
        >>> sector = get_cik_sector(320193)  # Apple
        >>> print(sector)
        3571  # Electronic computers
    """
    companies_df = _load_companies_data()
    company_row = companies_df[companies_df['cik_str'] == cik]

    if company_row.empty:
        return None

    return int(company_row.iloc[0]['industry'])


def get_sector_name(sector_id: int) -> Optional[str]:
    """
    Get the industry title for a SIC sector code.

    Args:
        sector_id: SIC industry code

    Returns:
        Industry title string, or None if sector not found

    Example:
        >>> name = get_sector_name(3571)
        >>> print(name)
        "ELECTRONIC COMPUTERS"
    """
    industries_df = _load_industries_data()
    sector_row = industries_df[industries_df['SIC Code'] == sector_id]

    if sector_row.empty:
        return None

    return sector_row.iloc[0]['Industry Title']


def get_sector_company_count(sector_id: int) -> int:
    """
    Get the number of companies in a specific SIC sector.

    Args:
        sector_id: SIC industry code

    Returns:
        Number of companies in the sector

    Example:
        >>> count = get_sector_company_count(3571)
        >>> print(count)
        5  # Number of computer companies in dataset
    """
    return len(get_sector_ciks(sector_id))


def list_available_sectors() -> pd.DataFrame:
    """
    Get a DataFrame of all available SIC sectors with their details.

    Returns:
        DataFrame with columns: SIC Code, Office, Industry Title, Company Count

    Example:
        >>> sectors = list_available_sectors()
        >>> print(sectors.head())
    """
    industries_df = _load_industries_data()
    companies_df = _load_companies_data()

    # Count companies per sector
    sector_counts = companies_df.groupby('industry').size().reset_index(name='Company Count')
    sector_counts.rename(columns={'industry': 'SIC Code'}, inplace=True)

    # Merge with industry details
    result = industries_df.merge(sector_counts, on='SIC Code', how='left')
    result['Company Count'] = result['Company Count'].fillna(0).astype(int)

    return result.sort_values('SIC Code')


def get_company_info(cik: int) -> Optional[Dict[str, any]]:
    """
    Get complete company information for a CIK.

    Args:
        cik: Company CIK identifier

    Returns:
        Dictionary with company details, or None if not found

    Example:
        >>> info = get_company_info(320193)
        >>> print(info)
        {'cik': 320193, 'ticker': 'AAPL', 'title': 'Apple Inc.', 'industry': 3571}
    """
    companies_df = _load_companies_data()
    company_row = companies_df[companies_df['cik_str'] == cik]

    if company_row.empty:
        return None

    row = company_row.iloc[0]
    return {
        'cik': int(row['cik_str']),
        'ticker': row['ticker'],
        'title': row['title'],
        'industry': int(row['industry'])
    }