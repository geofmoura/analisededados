from plots.plots_comex_year import plots_comex_year
from plots.plots_bloco import generate_bloco_economico_plots
from plots.plots_exchange import generate_exchange_plots
from plots.plots_top5_comex import top5_import_counties


generate_exchange_plots()
top5_import_counties()
plots_comex_year()
generate_bloco_economico_plots()
