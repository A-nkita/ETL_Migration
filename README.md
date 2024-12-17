# MySQL to MSSQL Data Migration Tool

## Overview
This tool automates the process of migrating data from a MySQL table to an MSSQL table.  
It supports:
- Data transformation
- Error handling
- Logging (console + file-based logs)

## Features
1. Connects to MySQL and MSSQL databases.
2. Reads data from a MySQL source table.
3. Transforms and inserts the data into a specified MSSQL destination table.
4. Provides detailed logs using Python's `logging` module.

---

## Prerequisites
- Python 3.8 or higher
- MySQL Database
- MSSQL Server (Ensure ODBC driver is installed)
- Required Python libraries

---

## Installation

1. Clone the repository:
   ```bash
   git clone <your_repo_link>
   cd MySQL_MSSL_Migration


## License
This project is licensed under the [MIT License](LICENSE).
