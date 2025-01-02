# Useful Alembic Commands

Here’s a detailed list of useful Alembic commands and their explanations. Alembic is a powerful tool for database migrations in SQLAlchemy, and these commands are used for managing and applying schema changes to your database.

## 1. `alembic init <directory>`
   - **Purpose**: Initializes a new Alembic environment in the specified directory.
   - **Usage**:
     ```bash
     alembic init alembic
     ```
   - **What it does**: Creates the Alembic configuration file (`alembic.ini`) and a migrations folder with the default `env.py` script, where migration scripts will be generated.

## 2. `alembic revision --autogenerate -m "<message>"`
   - **Purpose**: Generates a new migration script by comparing the current state of the database with the models in your code.
   - **Usage**:
     ```bash
     alembic revision --autogenerate -m "Create users table"
     ```
   - **What it does**: 
     - Automatically generates a new migration script based on changes in the SQLAlchemy models.
     - It creates a new file in the `alembic/versions` folder with the specified message.
     - **Important**: Review the generated migration to ensure it matches the changes you expect.

## 3. `alembic upgrade <revision>`
   - **Purpose**: Applies a migration or migrates to a specific version.
   - **Usage**:
     ```bash
     alembic upgrade head
     ```
     Or to migrate to a specific revision:
     ```bash
     alembic upgrade <revision_id>
     ```
   - **What it does**:
     - Applies the migration scripts up to the specified revision (`head` for the latest revision).
     - Executes the schema changes in the database (e.g., creating tables, altering columns).
     - Can be used to upgrade or apply a specific migration to the database.

## 4. `alembic downgrade <revision>`
   - **Purpose**: Rolls back (downgrades) the database to a previous migration revision.
   - **Usage**:
     ```bash
     alembic downgrade -1  # Downgrades by one revision
     alembic downgrade <revision_id>  # Downgrades to a specific revision
     ```
   - **What it does**:
     - Rolls back the database schema to the specified revision, undoing the changes made by the migration scripts since that point.
     - You can also downgrade to a specific migration version using the revision ID.

## 5. `alembic current`
   - **Purpose**: Shows the current revision of the database.
   - **Usage**:
     ```bash
     alembic current
     ```
   - **What it does**: 
     - Displays the current version (revision) of the database schema.
     - Helps you see the database's current migration state.

## 6. `alembic history`
   - **Purpose**: Shows the history of migrations.
   - **Usage**:
     ```bash
     alembic history --verbose
     ```
   - **What it does**:
     - Displays a list of all migration revisions.
     - With `--verbose`, it also includes detailed information about each revision (e.g., description, date created).

## 7. `alembic revision --autogenerate --sql`
   - **Purpose**: Generates a SQL script for the migration rather than applying it directly to the database.
   - **Usage**:
     ```bash
     alembic revision --autogenerate --sql -m "Migration description"
     ```
   - **What it does**:
     - Instead of applying the migration, this command will output a SQL file (`migration.sql`) that contains the SQL commands to be executed on the database.
     - Useful for generating migration scripts that can be manually reviewed or applied in a different environment.

## 8. `alembic upgrade head --sql`
   - **Purpose**: Generates SQL for the migrations and outputs it to a file.
   - **Usage**:
     ```bash
     alembic upgrade head --sql > migration.sql
     ```
   - **What it does**:
     - Generates SQL for all migrations up to the `head` and writes it to `migration.sql`.
     - This is useful if you want to execute the SQL manually or in environments where Alembic cannot directly apply the migrations.

## 9. `alembic merge -m "<message>" <revision1> <revision2>`
   - **Purpose**: Merges two branches of the migration history.
   - **Usage**:
     ```bash
     alembic merge -m "Merge branches" <revision1> <revision2>
     ```
   - **What it does**:
     - Used when two different branches of migration histories diverge, and you need to merge them into a single linear history.
     - This is necessary when multiple people are working on migrations that result in different branches.

## 10. `alembic show <revision_id>`
   - **Purpose**: Shows the details of a specific migration.
   - **Usage**:
     ```bash
     alembic show <revision_id>
     ```
   - **What it does**:
     - Displays the details of a specific revision, including the description and the commands it contains.

## 11. `alembic stamp <revision>`
   - **Purpose**: Marks the database as having been upgraded to a specific revision without actually running the migration.
   - **Usage**:
     ```bash
     alembic stamp head
     alembic stamp <revision_id>
     ```
   - **What it does**:
     - Useful when you need to manually mark the database as having a certain revision, without actually applying the migration.
     - This is typically used when setting up a new database or skipping certain migrations (e.g., when you’ve manually applied the schema changes outside of Alembic).

## 12. `alembic upgrade head --sql > migration.sql`
   - **Purpose**: Generate SQL script for applying the migration.
   - **Usage**:
     ```bash
     alembic upgrade head --sql > migration.sql
     ```
   - **What it does**:
     - This generates a SQL script that you can manually apply to the database.
     - This is helpful if you're working in an environment where you cannot directly run Alembic commands (e.g., production servers) or if you want to review the migration SQL first.

## 13. `alembic downgrade -1 --sql > migration_down.sql`
   - **Purpose**: Generate SQL script for downgrading by one migration.
   - **Usage**:
     ```bash
     alembic downgrade -1 --sql > migration_down.sql
     ```
   - **What it does**:
     - Generates the SQL for rolling back one migration.
     - This can be useful for undoing changes in a controlled manner in environments where direct execution of Alembic is not preferred.

## 14. `alembic revision --head-only --sql`
   - **Purpose**: Generate SQL for only the head migration.
   - **Usage**:
     ```bash
     alembic revision --head-only --sql -m "Migration description"
     ```
   - **What it does**:
     - Generates SQL for only the head migration, which is useful for understanding the last set of changes without pulling in older revisions.

---

## Summary of Commonly Used Alembic Commands

| Command                           | Description                                                                                      |
|-----------------------------------|--------------------------------------------------------------------------------------------------|
| `alembic init <directory>`        | Initializes a new Alembic environment.                                                           |
| `alembic revision -m "<message>"` | Creates a new migration script with the given message.                                           |
| `alembic upgrade <revision>`      | Upgrades the database to a specific revision (e.g., `head` for latest).                          |
| `alembic downgrade <revision>`    | Rolls back the database to a specific revision.                                                  |
| `alembic current`                 | Shows the current revision in the database.                                                      |
| `alembic history`                 | Shows the migration history.                                                                     |
| `alembic merge`                   | Merges two branches of migration history into one.                                               |
| `alembic show <revision_id>`      | Displays details for a specific migration.                                                       |
| `alembic stamp <revision>`        | Marks the database as upgraded to a specific revision without running the migration.             |
| `alembic upgrade head --sql`      | Generates a SQL script for applying the latest migration.                                         |

These are the core Alembic commands you'll use to manage database migrations in your project. You can combine these commands to automate migrations, review the migration history, and troubleshoot schema changes efficiently.
