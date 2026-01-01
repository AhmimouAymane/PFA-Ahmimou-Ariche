# How to Create the Database

Use one of these methods to create the MySQL database:

## Method 1: Using Python Script (Easiest)

1. Make sure you know your MySQL root password
2. Open PowerShell in the `backend` folder
3. Run one of these commands:

**Option A - Pass password as argument:**
```powershell
python scripts/create_db_simple.py YOUR_PASSWORD
```

**Option B - Use environment variable:**
```powershell
$env:MYSQL_PASSWORD="YOUR_PASSWORD"
python scripts/create_db_simple.py
```

Or:
```powershell
$env:MYSQL_ROOT_PASSWORD="YOUR_PASSWORD"
python scripts/create_db_simple.py
```

Replace `YOUR_PASSWORD` with your actual MySQL root password.

## Method 2: Using MySQL Command Line

1. Open MySQL command line client or terminal
2. Connect as root:
```bash
mysql -u root -p
```
3. Enter your password when prompted
4. Create the database:
```sql
CREATE DATABASE chatbot_admin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
5. Exit MySQL:
```sql
EXIT;
```

## Method 3: Using MySQL Workbench

1. Open MySQL Workbench
2. Connect to your MySQL server
3. Click on "Server" → "Data Import" or use SQL Editor
4. Run the following SQL:
```sql
CREATE DATABASE chatbot_admin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Method 4: Using DBeaver or Another Client

1. Download DBeaver Community Edition (free) or use your preferred MySQL client
2. Connect to MySQL
3. Run: `CREATE DATABASE chatbot_admin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

## After Creating Database

Update your `backend/.env` file:

```
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/chatbot_admin
```

Then continue with the setup!

## Troubleshooting

- **MySQL service not running**: 
  - Windows: Open Services (services.msc) and start MySQL service
  - Check MySQL is listening on port 3306

- **Connection refused**:
  - Verify MySQL is installed and running
  - Check your username and password
  - Ensure MySQL is accessible on localhost:3306

- **pymysql not found**:
  - Install it: `pip install pymysql`
