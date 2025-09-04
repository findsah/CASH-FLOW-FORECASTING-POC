# Cash Flow Forecaster

A comprehensive web application for analyzing cash flow, forecasting future finances, and discovering investment opportunities based on your bank statements.

## Features

- **Bank Statement Analysis**: Upload CSV or PDF bank statements for automatic processing
- **Cash Flow Visualization**: Interactive charts showing income, expenses, and trends
- **Financial Forecasting**: Predict future cash flow based on historical data
- **Investment Recommendations**: Get personalized investment suggestions based on your financial profile
- **Expense Categorization**: Automatic categorization of transactions
- **Interactive Dashboard**: Clean, modern interface for financial insights

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cashflow_forecaster
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and go to: http://localhost:5000

## Usage

1. **Upload Bank Statement**
   - Click the upload area or drag and drop your bank statement (CSV or PDF)
   - The system will automatically process and analyze your transactions

2. **View Financial Overview**
   - See your total income, expenses, and net cash flow
   - Analyze spending patterns with interactive charts

3. **Explore Investment Opportunities**
   - Get personalized investment recommendations
   - View suggested asset allocation based on your risk profile

4. **Forecast Future Cash Flow**
   - See projected income and expenses for the next 6 months
   - Plan your finances with data-driven insights

## Supported File Formats

- **CSV**: Ensure your CSV has columns for date, description, and amount
- **PDF**: Most bank statement PDFs are supported (text-based PDFs work best)

## Customization

### Adding Custom Categories
Edit the `app.py` file to add or modify expense categories in the `categorize_transactions` function.

### Adjusting Investment Strategy
Modify the `get_investment_suggestions` function in `app.py` to adjust the investment allocation based on different risk profiles.

## Troubleshooting

- **Upload Issues**: Ensure your file is not password protected and is in a supported format
- **Missing Transactions**: Some PDFs with complex layouts might not be parsed correctly
- **Performance**: For large statements, processing might take a few moments

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This application is for informational purposes only and should not be considered as financial advice. Always consult with a qualified financial advisor before making investment decisions.
