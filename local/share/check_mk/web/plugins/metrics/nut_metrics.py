from cmk.gui.i18n import _
from cmk.gui.plugins.metrics import (
    metric_info,
    graph_info,
)

metric_info["nut_charge"] = {
    "title": _("Charge"),
    "unit": "%",
    "color": "15/a",
}

metric_info["nut_runtime"] = {
    "title": _("Runtime"),
    "unit": "s",
    "color": "14/b",
}

metric_info["nut_voltage"] = {
    "title": _("Voltage"),
    "unit": "v",
    "color": "15/a",
}

metric_info["nut_load"] = {
    "title": _("Load"),
    "unit": "%",
    "color": "16/a",
}
