from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Integer,
    TextAscii,
)
from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersOperatingSystem,
)

def _item_valuespec_nut():
    return TextAscii(title=_("Variable name"))

def _parameter_valuespec_nut():
    return Dictionary(
        elements=[
            ("nut_warning_voltage", Tuple(
                title = _("Battery voltage"),
                help = _("The warning levels when battery voltage gets too low."),
                elements = [
                    Integer(title = _("Warning below")),
                    Integer(title = _("Critical below"))
                ],
            )),
            ("nut_warning_input_voltage_low", Tuple(
                title = _("Input voltage low"),
                help = _("The warning levels when input voltage gets too low."),
                elements = [
                    Integer(title = _("Warning below")),
                    Integer(title = _("Critical below"))
                ],
            )),
            ("nut_warning_input_voltage_high", Tuple(
                title = _("Input voltage high"),
                help = _("The warning levels when input voltage gets too high."),
                elements = [
                    Integer(title = _("Warning above")),
                    Integer(title = _("Critical above"))
                ],
            )),
            ("nut_warning_charge", Tuple(
                title = _("Charge"),
                help = _("The warning levels when battery charge gets too low."),
                elements = [
                    Integer(title = _("Warning below")),
                    Integer(title = _("Critical below"))
                ],
            )),
            ("nut_warning_runtime", Tuple(
                title = _("Runtime"),
                help = _("The warning levels when battery runtime gets too low."),
                elements = [
                    Integer(title = _("Warning below")),
                    Integer(title = _("Critical below"))
                ],
            )),
            ("nut_warning_load", Tuple(
                title = _("Load"),
                help = _("The warning levels when UPS load gets too high."),
                elements = [
                    Integer(title = _("Warning above")),
                    Integer(title = _("Critical above"))
                ],
            )),
        ],
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="nut_parameters",
        group=RulespecGroupCheckParametersOperatingSystem,
        match_type="dict",
        item_spec=_item_valuespec_nut,
        parameter_valuespec=_parameter_valuespec_nut,
        title=lambda: _("Paramters for NUT"),
    )
)
