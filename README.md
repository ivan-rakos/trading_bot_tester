# Trading Bot Tester

> Herramienta ligera para backtesting y pruebas de estrategias de trading con datos históricos (CSV).

## Descripción

Este proyecto contiene utilidades y un entorno simple para probar estrategias de trading usando archivos CSV de series temporales (OHLCV). Incluye scripts de ayuda (aux\_\*.py), módulos de indicadores y un ejecutable principal para lanzar pruebas.

## Estructura del repositorio

- `main.py` — Punto de entrada principal (uso general).
- `tester.py` — Script de pruebas/backtesting.
- `indicadores.py` — Cálculo de indicadores técnicos.
- `utils.py`, `dates.py` — Utilidades auxiliares.
- `aux_binance.py`, `aux_bingx.py`, `bingx.py` — Integraciones/auxiliares para exchanges.
- `resources/` — Carpeta con datos históricos por símbolo (CSV). Ej.: `resources/RUNE-USDT/2024-04_30m.csv`.

## Requisitos

- Python 3.8 o superior
- Recomendado: `pandas`, `numpy` (añade otras dependencias según tus necesidades)

Instalar dependencias (ejemplo):

```bash
python -m venv .venv
.venv\\Scripts\\activate   # Windows
pip install --upgrade pip
pip install pandas numpy
```

Si prefieres usar un `requirements.txt`, crea el archivo y ejecuta `pip install -r requirements.txt`.

## Formato de los datos

Los CSV en `resources/<SIMBOLO>/` deberían contener columnas tipo: `timestamp`, `open`, `high`, `low`, `close`, `volume`. Ajusta los nombres de columnas en `utils.py` o donde se carguen si tu formato difiere.

## Uso básico

1. Coloca los CSV en `resources/<SIMBOLO>/`.
2. Ejecuta el script principal o el tester:

```bash
python main.py
# o
python tester.py
```

Los scripts analizarán los datos y ejecutarán las rutinas de backtest/estrategias implementadas.
