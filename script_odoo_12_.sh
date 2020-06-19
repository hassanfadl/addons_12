#!/bin/bash
echo -e "actualizar sistema"

apt-get update && apt-get upgrade -y


echo -e "crear usuario"
sudo userdel -r odoo
adduser --system --home=/opt/odoo --group odoo

echo -e "actualizar sistema"
sudo apt install postgresql postgresql-contrib


echo -e "actualizar sistema"

echo -e "actualizar sistema"

echo -e "actualizar sistema"

echo -e "actualizar sistema"

echo -e "actualizar sistema"