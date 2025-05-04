# Генератор конфигураций базовой станции

![Build Status](https://github.com/Salvatore112/BaseConfigGen/actions/workflows/ci.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Возможности

- Парсинг UML-моделей из XML
- Генерация конфигураций в различных форматах:
  - `config.xml` - внутренняя конфигурация базовой станции
  - `meta.json` - метаданные классов для отображения в UI
  - `delta.json` - отслеживание изменений конфигурации
  - `res_patched_config.json` - модифицированные конфигурации
- Проверка согласованности конфигураций

## Требования

- Python 3.11+

## Запуск (для python3.11)

```bash
git clone https://github.com/Salvatore112/BaseConfigGen.git
cd base-station-config-generator
python3.11 ./main.py
