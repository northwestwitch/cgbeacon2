# -*- coding: utf-8 -*-
import logging
import urllib.request
import zlib

LOG = logging.getLogger(__name__)


def ebi_genenames():
    """Fetch the hgnc genes file from
        ftp://ftp.ebi.ac.uk/pub/databases/genenames/new/tsv/hgnc_complete_set.txt

    Returns:
        hgnc_gene_lines(list(str))
    """

    file_name = "hgnc_complete_set.txt"
    url = f"ftp://ftp.ebi.ac.uk/pub/databases/genenames/new/tsv/{file_name}"
    LOG.info("Fetching HGNC genes from %s", url)

    hgnc_lines = fetch_resource(url)
    hgnc_lines


def fetch_resource(url, json=False):
    """Fetch a resource and return the resulting lines in a list or a json object
    Send file_name to get more clean log messages

    Args:
        url(str)
        json(bool): if result should be in json

    Returns:
        data
    """
    data = None
    if url.startswith("ftp"):
        # requests do not handle ftp
        response = urllib.request.urlopen(url, timeout=20)
        if isinstance(response, Exception):
            raise response
        data = response.read().decode("utf-8")
        LOG.error(data)
        return data.split("\n")

    response = get_request(url)

    if json:
        LOG.info("Return in json")
        data = response.json()
    else:
        content = response.text
        LOG.info(response.text)
        if response.url.endswith(".gz"):
            LOG.info("gzipped!")
            encoded_content = b"".join(chunk for chunk in response.iter_content(chunk_size=128))
            content = zlib.decompress(encoded_content, 16 + zlib.MAX_WBITS).decode("utf-8")

        data = content.split("\n")
    return data
