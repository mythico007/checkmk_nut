# import necessary functions
from .agent_based_api.v1 import *

def discover_nut(section):
# create all necessary services
    section = clean_section(section)
    for ups_name, variable, _ in section:
        yield Service(item=title_generator(ups_name, variable))

def check_nut(item, params, section):
# check functions
# the transmitted values are processed here
    section = clean_section(section)

    for ups_name, variable, value in section:
        if title_generator(ups_name, variable) == item:
            if variable == "battery.charge":
                value = float(value)
# fetch rule values
                (lowwarn, lowcrit)  = params["nut_warning_charge"]
                yield Metric(
                    "nut_charge",
                    value,
                    levels=(lowwarn, lowcrit),
                    boundaries=(0,100))
                if value <= lowcrit:
                    yield Result(state = State.CRIT,
                                 summary = f"[{value}%] Battery low / warn: {lowwarn} % / crit: {lowcrit} %")
                elif value <= lowwarn:
                    yield Result(state = State.WARN,
                                 summary = f"[{value}%] Battery running low / warn: {lowwarn} % / crit: {lowcrit} %")
                else:
                    yield Result(state = State.OK,
                                 summary = f"[{value}%] Battery good / warn: {lowwarn} % / crit: {lowcrit} %")
                return
            if variable == "battery.runtime":
                value = float(value)
# fetch rule values
                (lowwarn, lowcrit)  = params["nut_warning_runtime"]
                yield Metric(
                    "nut_runtime",
                    value,
                    levels=(lowwarn*60, lowcrit*60),
                    boundaries=(0,None))
                if value <= lowcrit:
                    s = State.CRIT
                elif value <= lowwarn:
                    s = State.WARN
                else:
                    s = State.OK
                yield Result(state = s,
                             summary = f"Battery runtime is {render.timespan(value)} / warn: {lowwarn} minutes / crit: {lowcrit} minutes")
                return
            if variable == "battery.voltage":
                value = float(value)
# fetch rule values
                (lowwarn, lowcrit)  = params["nut_warning_voltage"]
                yield Metric(
                    "nut_voltage",
                    value,
                    levels=(lowwarn, lowcrit),
                    boundaries=(0,30))
                if value <= lowcrit:
                    s = State.CRIT
                elif value <= lowwarn:
                    s = State.WARN
                else:
                    s = State.OK
                yield Result(state = s,
                             summary = f"Battery voltage is {value} volts / warn: {lowwarn} / crit: {lowcrit}")
                return
            if variable == "input.voltage":
                value = float(value)
# fetch rule values
                (lowwarn, lowcrit) = params["nut_warning_input_voltage_low"]
                (highwarn, highcrit) = params["nut_warning_input_voltage_high"]
                yield Metric(
                    "nut_voltage",
                    value,
                    levels=(lowwarn, lowcrit),
                    boundaries=(0,400))
                if value <= lowcrit:
                    yield Result(state = State.CRIT,
                                 summary = f"[{value}V] Input voltage too low")
                elif value <= lowwarn:
                    yield Result(state = State.WARN,
                                 summary = f"[{value}V] Input voltage low")
                elif value >= highcrit:
                    yield Result(state = State.CRIT,
                                 summary = f"[{value}V] Input voltage too high")
                elif value >= highwarn:
                    yield Result(state = State.WARN, 
                                 summary = f"[{value}V] Input voltage high")
                else:
                    yield Result(state = State.OK,
                                 summary = f"[{value}V] Input voltage good / low: warn: {lowwarn}, crit: {lowcrit} / high: warn: {highwarn}, crit: {highcrit}")
                return
            if variable == "ups.load":
                value = float(value)
# fetch rule values
                (highwarn, highcrit) = params["nut_warning_load"]
                yield Metric(
                    "nut_load",
                    value,
                    levels=(highwarn, highcrit),
                    boundaries=(0,100))
                if value >= highcrit:
                    yield Result(state = State.CRIT,
                                 summary = f"[{value}%] UPS load high / warn: {highwarn} / crit: {highcrit}")
                elif value >= highwarn:
                    yield Result(state = State.WARN,
                                 summary = f"[{value}%] UPS load high / warn: {highwarn} / crit: {highcrit}")
                else:
                    yield Result(state = State.OK,
                                 summary = f"[{value}%] UPS load good / warn: {highwarn} / crit: {highcrit}")
                return
            if variable == "ups.status":
                if value == "OL":
                    yield Result(state = State.OK,
                                 summary = f"[{value}] online, fully charged")
                elif value == "OL CHRG":
                    yield Result(state = State.WARN,
                                 summary = f"[{value}] online, charging")
                elif value == "OL OFF":
                    yield Result(state = State.WARN,
                                 summary = f"[{value}] online offline")
                elif value == "OL DISCHRG":
                    yield Result(state = State.WARN,
                                 summary = f"[{value}] online, discharging")
                elif value == "OB DISCHRG":
                    yield Result(state = State.WARN,
                                 summary = f"[{value}] on battery, discharging")
                elif value == "OL LB":
                    yield Result(state = State.CRIT,
                                 summary = f"[{value}] on battery, low battery")
                elif value == "FSD OL CHRG":
                    yield Result(state = State.OK,
                                 summary = f"[{value}] forced shutdown, online, charging")
                else:
                    yield Result(state = State.CRIT,
                                 summary = f"[{value}] unknown state")
                return
            yield Result(state=State.OK, summary=value)
            return


def title_generator(ups_name, variable):
# generate service name: ups_name + parametername
    return f"{ups_name} - {variable}"

def clean_section(section):
# clean up matrix:
# row 1 = upsname
# row 2 = parametername without ":" at the end
# row 3..n = parameter values joined with ' '
    items = []
    for line in section:
        items.append([line[0], line[1][:-1], ' '.join(line[2:])])
    return items

register.check_plugin(
# declare checks
    name = "nut",
    service_name = "NUT %s",
    discovery_function = discover_nut,
    check_function = check_nut,
    check_default_parameters = {"nut_warning_voltage": (23, 15),
                                "nut_warning_input_voltage_low": (200, 170),
                                "nut_warning_input_voltage_high": (250, 280),
                                "nut_warning_charge": (30, 15),
                                "nut_warning_runtime": (10, 5),
                                "nut_warning_load": (70, 90)},
    check_ruleset_name = "nut_parameters",
)

