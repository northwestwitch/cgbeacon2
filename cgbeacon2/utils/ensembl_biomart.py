"""Code for talking to ensembl rest API"""
import logging

BIOMART_37 = "http://grch37.ensembl.org/biomart/martservice?query="
BIOMART_38 = "http://ensembl.org/biomart/martservice?query="
CHROMOSOMES = [str(num) for num in range(1, 23)] + ["X", "Y", "MT"]
ATTRIBUTES = [
    "chromosome_name",
    "start_position",
    "end_position",
    "ensembl_gene_id",
    "hgnc_symbol",
    "hgnc_id",
]

LOG = logging.getLogger(__name__)


class EnsemblBiomartClient:
    """Class to handle requests to the ensembl biomart api"""

    def __init__(self, build="37"):
        """Initialise a ensembl biomart client"""
        self.server = BIOMART_37
        if build == "38":
            self.server = BIOMART_38
        self.filters = {"chromosome_name": CHROMOSOMES}
        self.attributes = [
            "chromosome_name",
            "start_position",
            "end_position",
            "ensembl_gene_id",
            "hgnc_symbol",
            "hgnc_id",
        ]
        self.xml = self._create_biomart_xml()
        self.header = True
        self.attribute_to_header = {
            "chromosome_name": "Chromosome/scaffold name",
            "ensembl_gene_id": "Gene stable ID",
            "start_position": "Gene start (bp)",
            "end_position": "Gene end (bp)",
            "hgnc_symbol": "HGNC symbol",
            "hgnc_id": "HGNC ID",
        }

    def _create_biomart_xml(self):
        """Convert biomart query params into biomart xml query

        Accepts:
            filters(dict): keys are filter names and values are filter values
            attributes(list): a list of attributes

        Returns:
            xml: a query xml file

        """
        filter_lines = self._xml_filters()
        attribute_lines = self._xml_attributes()
        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            "<!DOCTYPE Query>",
            '<Query  virtualSchemaName = "default" formatter = "TSV" header = "0" uniqueRows'
            ' = "0" count = "" datasetConfigVersion = "0.6" completionStamp = "1">',
            "",
            '\t<Dataset name = "hsapiens_gene_ensembl" interface = "default" >',
        ]
        for line in filter_lines:
            xml_lines.append("\t\t" + line)
        for line in attribute_lines:
            xml_lines.append("\t\t" + line)
        xml_lines += ["\t</Dataset>", "</Query>"]

        return "\n".join(xml_lines)

    def _xml_filters(self):
        """Creates a filter line for the biomart xml document

        Returns:
            formatted_lines(list[str]): List of formatted xml filter lines
        """
        formatted_lines = []
        for filter_name in self.filters:
            value = self.filters[filter_name]
            if isinstance(value, str):
                formatted_lines.append(
                    '<Filter name = "{0}" value = "{1}"/>'.format(filter_name, value)
                )
            else:
                formatted_lines.append(
                    '<Filter name = "{0}" value = "{1}"/>'.format(filter_name, ",".join(value))
                )

        return formatted_lines

    def _xml_attributes(self):
        """Creates an attribute line for the biomart xml document

        Returns:
            formatted_lines(list(str)): list of formatted xml attribute lines
        """
        formatted_lines = []
        for attr in self.attributes:
            formatted_lines.append('<Attribute name = "{}" />'.format(attr))
        return formatted_lines
