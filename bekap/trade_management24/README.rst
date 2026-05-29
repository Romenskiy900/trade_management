# Trade Management (Odoo Module)

## Overview

Trade Management is an Odoo module for managing the trading process, including receipts, sales, product price management, and reports.

## Features

### Receipts
- Incoming goods management
- Automatic creation of stock movements (stock picking / stock moves)
- Stock validation before posting the document
- After posting, the document cannot be edited or deleted

### Sales
- Sales management
- Stock availability check
- Automatic creation of stock movements

### Price Management
- Price lists with time-based tracking
- Automatic product price synchronization

### Reports
- Receipt report grouped by:
  - date
  - partner
  - product
- Date range filtering via wizard

### Wizards
- Mass product category update
- Receipt report wizard with date filtering

## Business Rules

- Posted documents cannot be edited or deleted
- Quantity must be greater than 0
- Price must be greater than 0
- Stock is checked before sales
- Product price is automatically updated from price lists

## Technical Features

- Uses ir.sequence for document numbering
- Mixin for reusable document logic
- Computed fields (sum)
- Onchange logic for dynamic price updates
- SQL queries for stock optimization (stock.quant)
- Odoo reporting system (_get_report_values)
- Post-init hook for automatic demo data processing

## Security

- Record rules restrict access:
  - Managers see only their own documents
  - Admins have full access
- User groups control CRUD permissions

## Installation

1. Copy module into addons folder: trade_management
2. Restart Odoo server
3. Update apps list
4. Install module via Apps menu

## Dependencies

- stock
- product
- base

## Note

This module is created for learning and Odoo development practice. It demonstrates real business processes, stock handling, SQL optimization, and clean architecture design.

## Author

Custom Odoo Development Project