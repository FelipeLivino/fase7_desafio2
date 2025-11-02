# Use the official PostgreSQL image
FROM postgres:15-alpine

# The official postgres image will automatically run any .sql files
# in the /docker-entrypoint-initdb.d directory upon startup.
# This is a convenient way to initialize the database with a schema and data.

# Copy the SQL schema file to the initialization directory
COPY farmtech_schema.sql /docker-entrypoint-initdb.d/

# No CMD or ENTRYPOINT is needed as the base image already has one
# that handles starting PostgreSQL and running the init scripts.
