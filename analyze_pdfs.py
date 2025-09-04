import os
import PyPDF2
import pandas as pd
from datetime import datetime
import re

class BankStatementAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.filename = os.path.basename(file_path)
        self.transactions = []
        self.summary = {
            'filename': self.filename,
            'statement_period': None,
            'opening_balance': 0,
            'closing_balance': 0,
            'total_credits': 0,
            'total_debits': 0,
            'transaction_count': 0,
            'transactions': []
        }

    def extract_text_from_pdf(self):
        text = ""
        try:
            with open(self.file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading {self.filename}: {str(e)}")
        return text

    def analyze_statement(self):
        text = self.extract_text_from_pdf()
        
        # Extract statement period
        period_match = re.search(r'(?:statement|period)[^\n]*\n([^\n]+)', text, re.IGNORECASE)
        if period_match:
            self.summary['statement_period'] = period_match.group(1).strip()
            
        # Extract balances
        balance_matches = re.findall(r'(?:opening|closing|balance)[^\d£$]*(£?[\d,]+\.[\d]{2})', text, re.IGNORECASE)
        if len(balance_matches) >= 2:
            self.summary['opening_balance'] = float(balance_matches[0].replace('£', '').replace(',', ''))
            self.summary['closing_balance'] = float(balance_matches[-1].replace('£', '').replace(',', ''))
        
        # Extract transactions (simplified pattern - may need adjustment)
        transaction_pattern = r'(\d{1,2}/\d{1,2}/\d{2,4})\s+(.*?)\s+(£?[\d,]+\.[\d]{2})[\s\n]+(£?[\d,]+\.[\d]{2})?'
        transactions = re.findall(transaction_pattern, text, re.DOTALL)
        
        for t in transactions:
            try:
                date = datetime.strptime(t[0], '%d/%m/%Y').strftime('%Y-%m-%d')
                description = t[1].strip()
                amount = float(t[2].replace('£', '').replace(',', ''))
                balance = float(t[3].replace('£', '').replace(',', '')) if t[3] else None
                
                transaction = {
                    'date': date,
                    'description': description,
                    'amount': amount,
                    'balance': balance,
                    'type': 'credit' if amount >= 0 else 'debit'
                }
                
                self.summary['transactions'].append(transaction)
                
                if amount >= 0:
                    self.summary['total_credits'] += amount
                else:
                    self.summary['total_debits'] += abs(amount)
                    
                self.summary['transaction_count'] += 1
                
            except Exception as e:
                print(f"Error processing transaction: {t}, Error: {str(e)}")
        
        return self.summary

def analyze_all_statements():
    uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
    statements = [
        'Statement_521046_25886037_29_Aug_2025.pdf',
        'account-statement_2025-07-01_2025-09-03_en-gb_5bf676.pdf',
        'attachment.pdf'
    ]
    
    results = []
    
    for stmt in statements:
        file_path = os.path.join(uploads_dir, stmt)
        if os.path.exists(file_path):
            print(f"\nAnalyzing: {stmt}")
            analyzer = BankStatementAnalyzer(file_path)
            result = analyzer.analyze_statement()
            results.append(result)
            
            # Print summary
            print(f"Statement Period: {result.get('statement_period', 'N/A')}")
            print(f"Opening Balance: £{result.get('opening_balance', 0):,.2f}")
            print(f"Closing Balance: £{result.get('closing_balance', 0):,.2f}")
            print(f"Total Credits: £{result.get('total_credits', 0):,.2f}")
            print(f"Total Debits: £{result.get('total_debits', 0):,.2f}")
            print(f"Number of Transactions: {result.get('transaction_count', 0)}")
            
            # Save detailed transactions to CSV
            if result['transactions']:
                df = pd.DataFrame(result['transactions'])
                csv_filename = os.path.splitext(stmt)[0] + '.csv'
                df.to_csv(csv_filename, index=False)
                print(f"Transactions saved to: {csv_filename}")
    
    return results

if __name__ == "__main__":
    analyze_all_statements()
