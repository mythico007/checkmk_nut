from .agent_based_api.v1 import *


def discover_nut(section):
    section = clean_section(section)
    for ups_name, variable, _ in section:
        yield Service(item=title_generator(ups_name, variable))


def check_nut(item, section):
    section = clean_section(section)
    for ups_name, variable, value in section:
        if title_generator(ups_name, variable) == item:
            yield Result(state=State.OK, summary=value)
            return


def clean_section(section):
    items = []
    for line in section:
        items.append([line[0], line[1][:-1], ' '.join(line[2:])])
    return items


def title_generator(upsname, variable):
    return f"{upsname} - {variable}"


register.check_plugin(
    name="nut",
    service_name="NUT %s",
    discovery_function=discover_nut,
    check_function=check_nut,
)
