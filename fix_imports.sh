#!/bin/bash

# Script para substituir 'blog' por 'freeroad' em todos os arquivos Python
find ./backend/freeroad -type f -name "*.py" -exec sed -i '' 's/from blog\./from freeroad\./g' {} \;
find ./backend/freeroad -type f -name "*.py" -exec sed -i '' 's/import blog\./import freeroad\./g' {} \;

echo "Substituição concluída!"
