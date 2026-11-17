"""ParkEase - small in-memory model of the exit-payment rules R1 to R8."""
from dataclasses import dataclass

GRACE_MINUTES = 15
FIRST_HOUR = 100
EXTRA_HOUR = 60
CAP = 800
EV_DISCOUNT_PERCENT = 25
SERVICE_CHARGE = 20


@dataclass
class ExitResult:
    message: str = ""
    parking_fee: int = 0
    ev_discount: int = 0
    service_charge: int = 0
    total_paid: int = 0
    gate_open: bool = False
    receipt: str = ""


class ParkEase:
    def __init__(self):
        self._registered = set()
        self._driver = None          # logged-in driver
        self._plate = None           # linked vehicle
        self._electric = False
        self._wallet = 0

    # ---- account set-up -------------------------------------------------
    def register(self, driver):
        self._registered.add(driver)

    def login(self, driver):
        if driver in self._registered:
            self._driver = driver
            return True
        return False

    def logout(self):
        self._driver = None

    def link_vehicle(self, plate, electric):
        self._plate = plate
        self._electric = electric

    def set_wallet(self, rupees):
        self._wallet = rupees

    def wallet_balance(self):
        return self._wallet

    # ---- fee rules ------------------------------------------------------
    def parking_fee(self, minutes):
        """R2, R3 and R4: grace period, started hours, cap."""
        if minutes <= GRACE_MINUTES:
            return 0
        started_hours = -(-minutes // 60)          # round up
        fee = FIRST_HOUR + (started_hours - 1) * EXTRA_HOUR
        return min(fee, CAP)

    # ---- exit -----------------------------------------------------------
    def exit(self, plate, minutes_parked):
        # R1
        if self._driver is None:
            return ExitResult(message="Please log in to pay by wallet")
        if plate != self._plate:
            return ExitResult(message="No vehicle linked to this account")

        fee = self.parking_fee(minutes_parked)
        if fee == 0:                                # free exit, R6
            return ExitResult(message="Free exit - gate opening", gate_open=True)

        # R5: discount after the cap
        discount = fee * EV_DISCOUNT_PERCENT // 100 if self._electric else 0
 

        total = fee - discount + SERVICE_CHARGE     # R6

        # R7
        if self._wallet < total:
            return ExitResult(message="Insufficient wallet balance",
                              parking_fee=fee, ev_discount=discount,
                              service_charge=SERVICE_CHARGE)

        # R8
        self._wallet -= total
        receipt = (f"Parking fee Rs. {fee}\nEV discount Rs. {discount}\n"
                   f"Service charge Rs. {SERVICE_CHARGE}\nTotal Rs. {total}\n"
                   f"Wallet balance Rs. {self._wallet}")
        return ExitResult(message="Payment successful – gate opening",
                          parking_fee=fee, ev_discount=discount,
                          service_charge=SERVICE_CHARGE, total_paid=total,
                          gate_open=True, receipt=receipt)
