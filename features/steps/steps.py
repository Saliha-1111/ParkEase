import parse
from behave import given, when, then, register_type


# Custom parameter type: turns "1,000" into the integer 1000
@parse.with_pattern(r"\d[\d,]*")
def parse_amount(text):
    return int(text.replace(",", ""))


register_type(Amount=parse_amount)


def minutes_between(start, end):
    """Length of a stay in minutes, from two HH:MM clock times."""
    sh, sm = map(int, start.split(":"))
    eh, em = map(int, end.split(":"))
    return (eh * 60 + em) - (sh * 60 + sm)


def check(label, expected, actual):
    if isinstance(expected, int) and not isinstance(expected, bool):
        expected, actual = f"Rs. {expected}", f"Rs. {actual}"
    assert actual == expected, f"Expected {label}: {expected} but got {actual}"


# ---- Given ----------------------------------------------------------------
@given('the driver "{name}" is registered and logged in')
def registered_and_logged_in(context, name):
    context.app.register(name)
    context.app.login(name)


@given('the driver has linked the electric vehicle "{plate}"')
def link_electric(context, plate):
    context.plate = plate
    context.app.link_vehicle(plate, electric=True)


@given('the driver has linked the petrol vehicle "{plate}"')
def link_petrol(context, plate):
    context.plate = plate
    context.app.link_vehicle(plate, electric=False)


@given("the wallet balance is Rs. {amount:Amount}")
def set_wallet(context, amount):
    context.app.set_wallet(amount)


@given("the vehicle entered the plaza at {time}")
def set_entry_time(context, time):
    context.entry_time = time


@given("the vehicle was parked for {minutes:d} minutes")
def set_minutes(context, minutes):
    context.minutes = minutes


# ---- When -----------------------------------------------------------------
@when("the vehicle exits at {time}")
def exit_at(context, time):
    context.minutes = minutes_between(context.entry_time, time)
    context.result = context.app.exit(context.plate, context.minutes)


@when("the vehicle exits")
def exit_now(context):
    context.result = context.app.exit(context.plate, context.minutes)


# ---- Then -----------------------------------------------------------------
@then('the message should be "{message}"')
def check_message(context, message):
    check("message", message, context.result.message)


@then("the parking fee should be Rs. {amount:Amount}")
def check_fee(context, amount):
    check("parking fee", amount, context.result.parking_fee)


@then("the EV discount should be Rs. {amount:Amount}")
def check_discount(context, amount):
    check("EV discount", amount, context.result.ev_discount)


@then("the service charge should be Rs. {amount:Amount}")
def check_service(context, amount):
    check("service charge", amount, context.result.service_charge)


@then("the total paid should be Rs. {amount:Amount}")
def check_total(context, amount):
    check("total paid", amount, context.result.total_paid)


@then("the wallet balance should be Rs. {amount:Amount}")
def check_wallet(context, amount):
    check("wallet balance", amount, context.app.wallet_balance())


@then("the exit gate should be open")
def gate_open(context):
    check("gate open", True, context.result.gate_open)


@then("the exit gate should be closed")
def gate_closed(context):
    check("gate open", False, context.result.gate_open)
