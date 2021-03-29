import os

def create_directory(dir_path):
    if not os.path.isdir(dir_path):
        os.system(f'mkdir {dir_path}')
        print('output path created: ', dir_path)

def parse_fileName_vals(c, r, text_to_parse):
    ticker= r['ticker'] 
    cik_10dig = c.split("-")[0]
    filing_type = r['form']
    doc_reported_on = r['DateReported']
    filing_qrtr = r['FiscalQuarter End']
    doc_year = filing_qrtr[-4:]
    
    #print(doc_year)
    return ticker, cik_10dig, filing_type, filing_qrtr, doc_reported_on, doc_year
