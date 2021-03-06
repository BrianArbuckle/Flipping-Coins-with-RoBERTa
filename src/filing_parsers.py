## copied & adapted from data-engineering/parsers/filing_parsers.py (git)
import re

def quick_parse(filepath):
    parser = etree.XMLParser(recover=True, huge_tree=True)
    tree = etree.parse(filepath, parser)
    notags = etree.tostring(tree, encoding='utf8', method='text')
    return notags
def parse_10q(filepath, cik, year):
    """
    Parses the 10-Q passed. Returns a dictionary:
        body: The body of the 10-Q
    :param filepath:
    :return:
    """
    from bs4 import BeautifulSoup
    results = {}
    with open(filepath) as fp:
        soup = BeautifulSoup(fp, "lxml")
    # Get the header info
    results['headers'] = __parse_sec_header(soup, cik, year)
    results['documents'] = __parse_documents(soup)
    return results

def get_date(filingPath):
    """From FinBert"""
    accession_code = filingPath.split('/')[-2]
    ticker = filingPath.split('/')[-4]
    filing_type = filingPath.split('/')[-3]
    #print(accession_code, ticker, filing_type)
    code = accession_code+'.txt'
    with open(filingPath, 'r') as f:
        readlin = f.read()
    for i in readlin.split('\n'):
#         print(i)
        if code in i:
            date_extr = i.split(' : ')[1]
            return date_extr


def __parse_documents(soup):
    import time
    # Get all the douments
    result_documents = []
    documents = soup.find_all('document')

    for doc in documents:

        type_node = doc.find('type')
        if type_node:
            type_text = type_node.contents[0].strip()
            desc_node = type_node.find('description')
        else:
            type_text = 'NA'

        seq_node = doc.find('sequence')
        if seq_node:
            seq_text = seq_node.contents[0].strip()
        else:
            seq_text = str(int(time.time()))[-6:]

        if desc_node:
            desc_text = desc_node.contents[0]
        else:
            desc_text = ''

        if type_text in forms:
            is_10_q = True
        else:
            is_10_q = False

        if type_text not in ["XML", "GRAPHIC", "EXCEL", "ZIP"]:
            logging.debug("Parsing doucment type: {}".format(type_text))
            result_documents.append(
                {'is_10_q': is_10_q,
                 'type': type_text,
                 'sequence': seq_text,
                 'description': desc_text,
                 'document': __extract_document_text(doc)}
            )

    return result_documents

def __parse_sec_header(soup, cik, year):
    sec_header = soup.find("sec-header")

    if not sec_header:
        sec_header = soup

    result = {
        'cik': cik,
        'year': year,
    }
    result['accession_number'] = __get_line_item(sec_header, 'ACCESSION NUMBER:')
    result['conformed_period_of_report'] = __get_line_item(sec_header, 'CONFORMED PERIOD OF REPORT:')
    result['filed_as_of_date'] = __get_line_item(sec_header, 'FILED AS OF DATE:')
    result['company_confirmed_name'] = __get_line_item(sec_header, 'COMPANY CONFORMED NAME:')
    result['central_index_key'] = __get_line_item(sec_header, 'CENTRAL INDEX KEY:')
    result['standard_industrial_classification'] = __get_line_item(sec_header, 'STANDARD INDUSTRIAL CLASSIFICATION:')
    result['state_of_incorporation'] = __get_line_item(sec_header, 'STATE OF INCORPORATION:')
    result['fiscal_year_end'] = __get_line_item(sec_header, 'FISCAL QUARTER END:')

    return result

def __get_line_item(sec_header, attr_name):
    find_results = re.findall(attr_name + '(.*?)\n', str(sec_header))

    if find_results:
        return find_results[0].strip()
    else:
        return None
def __extract_document_text(document):

    tables = document.find_all('table')
    for table in tables:
        table.decompose()

    return document.get_text()