"""
Unit tests for sector_utils.py functionality.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.sector_utils import (
    get_sector_ciks,
    get_cik_sector,
    get_sector_name,
    get_sector_company_count,
    list_available_sectors,
    get_company_info
)

def test_sector_utils():
    print("Testing sector_utils.py functionality...\n")

    # Test get_sector_ciks
    print("1. Testing get_sector_ciks(3571) - Electronic computers:")
    ciks = get_sector_ciks(3571)
    print(f"   CIKs in sector 3571: {ciks}")
    print(f"   Number of companies: {len(ciks)}\n")

    # Test get_cik_sector
    print("2. Testing get_cik_sector(320193) - Apple:")
    apple_sector = get_cik_sector(320193)
    print(f"   Apple's sector: {apple_sector}\n")

    # Test get_sector_name
    print("3. Testing get_sector_name(3571):")
    sector_name = get_sector_name(3571)
    print(f"   Sector 3571 name: {sector_name}\n")

    # Test get_sector_company_count
    print("4. Testing get_sector_company_count(3571):")
    count = get_sector_company_count(3571)
    print(f"   Companies in sector 3571: {count}\n")

    # Test get_company_info
    print("5. Testing get_company_info(320193) - Apple:")
    apple_info = get_company_info(320193)
    print(f"   Apple info: {apple_info}\n")

    # Test list_available_sectors (first 5)
    print("6. Testing list_available_sectors() - first 5 sectors:")
    sectors = list_available_sectors()
    print(sectors.head())
    print(f"\n   Total sectors available: {len(sectors)}\n")

    # Test with another company
    print("7. Testing Microsoft (789019):")
    msft_sector = get_cik_sector(789019)
    msft_info = get_company_info(789019)
    msft_sector_name = get_sector_name(msft_sector) if msft_sector else "Unknown"
    print(f"   Microsoft sector: {msft_sector} ({msft_sector_name})")
    print(f"   Microsoft info: {msft_info}")

    if msft_sector:
        msft_sector_ciks = get_sector_ciks(msft_sector)
        print(f"   Other companies in Microsoft's sector: {len(msft_sector_ciks)} total")
        print(f"   First 5 CIKs: {msft_sector_ciks[:5]}\n")

    # Test error handling
    print("8. Testing error handling with invalid sector:")
    try:
        invalid_ciks = get_sector_ciks(99999)
        print(f"   Unexpected: {invalid_ciks}")
    except ValueError as e:
        print(f"   Expected error: {e}\n")

    print("All tests completed!")

if __name__ == "__main__":
    test_sector_utils()