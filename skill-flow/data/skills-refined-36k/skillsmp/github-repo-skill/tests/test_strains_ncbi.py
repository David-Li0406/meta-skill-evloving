"""Tests for NCBI utility functions."""

from cmm_ai_automation.strains.ncbi import NcbiLinkout, extract_xrefs_from_linkouts


class TestExtractXrefsFromLinkouts:
    """Tests for extract_xrefs_from_linkouts()."""

    def test_extract_bacdive_xref(self) -> None:
        """Test extracting BacDive xref from linkout."""
        linkouts: list[NcbiLinkout] = [
            {
                "provider": "BacDive",
                "name": "BacDive Strain 13546",
                "url": "https://bacdive.dsmz.de/strain/13546",
            }
        ]

        xrefs = extract_xrefs_from_linkouts(linkouts)

        assert len(xrefs) == 1
        assert "bacdive:13546" in xrefs

    def test_extract_multiple_bacdive_xrefs(self) -> None:
        """Test extracting multiple BacDive xrefs."""
        linkouts: list[NcbiLinkout] = [
            {
                "provider": "BacDive",
                "name": "BacDive",
                "url": "https://bacdive.dsmz.de/strain/100",
            },
            {
                "provider": "BacDive",
                "name": "BacDive",
                "url": "https://bacdive.dsmz.de/strain/200",
            },
        ]

        xrefs = extract_xrefs_from_linkouts(linkouts)

        assert len(xrefs) == 2
        assert "bacdive:100" in xrefs
        assert "bacdive:200" in xrefs

    def test_extract_bacdive_case_insensitive(self) -> None:
        """Test that provider name matching is case-insensitive."""
        linkouts: list[NcbiLinkout] = [
            {
                "provider": "bacdive",  # lowercase
                "name": "bacdive",
                "url": "https://bacdive.dsmz.de/strain/999",
            }
        ]

        xrefs = extract_xrefs_from_linkouts(linkouts)

        assert "bacdive:999" in xrefs

    def test_extract_biocyc_gcf_xref(self) -> None:
        """Test extracting BioCyc GCF xref."""
        linkouts: list[NcbiLinkout] = [
            {
                "provider": "BioCyc",
                "name": "BioCyc",
                "url": "http://biocyc.org/organism-summary?object=GCF_000346065",
            }
        ]

        xrefs = extract_xrefs_from_linkouts(linkouts)

        assert len(xrefs) >= 1
        assert "biocyc:GCF_000346065" in xrefs

    def test_extract_biocyc_taxon_xref(self) -> None:
        """Test extracting BioCyc taxon xref."""
        linkouts: list[NcbiLinkout] = [
            {
                "provider": "BioCyc",
                "name": "BioCyc",
                "url": "http://biocyc.org/organism-summary?object=12345",
            }
        ]

        xrefs = extract_xrefs_from_linkouts(linkouts)

        assert len(xrefs) >= 1
        assert "biocyc:taxon:12345" in xrefs

    def test_extract_lpsn_xref(self) -> None:
        """Test extracting LPSN species xref."""
        linkouts: list[NcbiLinkout] = [
            {
                "provider": "LPSN",
                "name": "LPSN",
                "url": "https://lpsn.dsmz.de/species/methylobacterium-extorquens",
            }
        ]

        xrefs = extract_xrefs_from_linkouts(linkouts)

        assert len(xrefs) == 1
        assert "lpsn:methylobacterium-extorquens" in xrefs

    def test_extract_lpsn_case_insensitive(self) -> None:
        """Test LPSN matching is case-insensitive."""
        linkouts: list[NcbiLinkout] = [
            {
                "provider": "lpsn",  # lowercase
                "name": "lpsn",
                "url": "https://lpsn.dsmz.de/species/test-species",
            }
        ]

        xrefs = extract_xrefs_from_linkouts(linkouts)

        assert "lpsn:test-species" in xrefs

    def test_extract_mixed_xrefs(self) -> None:
        """Test extracting multiple types of xrefs."""
        linkouts: list[NcbiLinkout] = [
            {
                "provider": "BacDive",
                "name": "BacDive",
                "url": "https://bacdive.dsmz.de/strain/100",
            },
            {
                "provider": "BioCyc",
                "name": "BioCyc",
                "url": "http://biocyc.org/organism-summary?object=GCF_000001",
            },
            {
                "provider": "LPSN",
                "name": "LPSN",
                "url": "https://lpsn.dsmz.de/species/test-bacterium",
            },
        ]

        xrefs = extract_xrefs_from_linkouts(linkouts)

        assert len(xrefs) == 3
        assert "bacdive:100" in xrefs
        assert "biocyc:GCF_000001" in xrefs
        assert "lpsn:test-bacterium" in xrefs

    def test_empty_linkouts_list(self) -> None:
        """Test that empty list returns empty xrefs."""
        linkouts: list[NcbiLinkout] = []

        xrefs = extract_xrefs_from_linkouts(linkouts)

        assert xrefs == []

    def test_unrecognized_provider_ignored(self) -> None:
        """Test that unrecognized providers are ignored."""
        linkouts: list[NcbiLinkout] = [
            {
                "provider": "UnknownDatabase",
                "name": "UnknownDatabase",
                "url": "http://example.com/something/123",
            }
        ]

        xrefs = extract_xrefs_from_linkouts(linkouts)

        assert xrefs == []

    def test_invalid_url_format_ignored(self) -> None:
        """Test that linkouts with invalid URL format are ignored."""
        linkouts: list[NcbiLinkout] = [
            {
                "provider": "BacDive",
                "name": "BacDive",
                "url": "https://bacdive.dsmz.de/no_strain_here",  # No /strain/ID pattern
            }
        ]

        xrefs = extract_xrefs_from_linkouts(linkouts)

        assert xrefs == []

    def test_deduplicates_xrefs(self) -> None:
        """Test that duplicate xrefs are deduplicated."""
        linkouts: list[NcbiLinkout] = [
            {
                "provider": "BacDive",
                "name": "BacDive",
                "url": "https://bacdive.dsmz.de/strain/100",
            },
            {
                "provider": "BacDive",
                "name": "BacDive",
                "url": "https://bacdive.dsmz.de/strain/100",  # Duplicate
            },
        ]

        xrefs = extract_xrefs_from_linkouts(linkouts)

        assert len(xrefs) == 1
        assert "bacdive:100" in xrefs

    def test_bacdive_url_detection(self) -> None:
        """Test BacDive detection by URL even if provider is different."""
        linkouts: list[NcbiLinkout] = [
            {
                "provider": "SomeOtherName",
                "name": "SomeOtherName",
                "url": "https://bacdive.dsmz.de/strain/999",
            }
        ]

        xrefs = extract_xrefs_from_linkouts(linkouts)

        # Should still detect BacDive from URL
        assert "bacdive:999" in xrefs

    def test_complex_lpsn_species_names(self) -> None:
        """Test LPSN with complex species names."""
        test_names = [
            "methylobacterium-extorquens",
            "escherichia-coli",
            "pseudomonas-putida-group",
        ]

        for name in test_names:
            linkouts: list[NcbiLinkout] = [
                {
                    "provider": "LPSN",
                    "name": "LPSN",
                    "url": f"https://lpsn.dsmz.de/species/{name}",
                }
            ]

            xrefs = extract_xrefs_from_linkouts(linkouts)

            assert f"lpsn:{name}" in xrefs

    def test_biocyc_gcf_with_various_formats(self) -> None:
        """Test BioCyc GCF extraction with various number formats."""
        gcf_ids = ["000000001", "000346065", "999999999"]

        for gcf_id in gcf_ids:
            linkouts: list[NcbiLinkout] = [
                {
                    "provider": "BioCyc",
                    "name": "BioCyc",
                    "url": f"http://biocyc.org/organism-summary?object=GCF_{gcf_id}",
                }
            ]

            xrefs = extract_xrefs_from_linkouts(linkouts)

            assert f"biocyc:GCF_{gcf_id}" in xrefs
