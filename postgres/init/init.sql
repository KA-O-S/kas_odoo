-- Create User odoo_live odoo.conf --> db_password
CREATE USER odoo_live WITH PASSWORD 'F7&8n52f^EF87&*3T$bxeMLoW';
ALTER USER odoo_live CREATEDB;


-- Create User odoo_stage odoo.conf --> db_password
CREATE USER odoo_stage WITH PASSWORD 'F7&8n52f^EF87&*3T$bxeMLoW';
ALTER USER odoo_stage CREATEDB;
