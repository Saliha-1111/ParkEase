from parkease import ParkEase


def before_scenario(context, scenario):
    context.app = ParkEase()
    context.plate = None
    context.entry_time = None
    context.minutes = None
    context.result = None
