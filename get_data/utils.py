import sys
from loguru import logger

def calculateTime(end_time: float, start_time: float):
    elapsed_time = end_time - start_time
    if elapsed_time > 60:
        return f'{elapsed_time/60:.2f} min'
    return f'{elapsed_time:.2f} sec'

def get_logger():
    logger.remove()
    logger.add(sys.stdout, level="DEBUG", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>", colorize=True, enqueue=True)
    return logger

def format_usd_mi(valor: float) -> str:
    valor_mi = valor / 1_000_000_000
    valor_formatado = f"{valor_mi:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"$ {valor_formatado} Bi"
