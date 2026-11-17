@negative
Feature: Wallet validation at the exit gate
  As a registered ParkEase driver
  I want to be told when my wallet cannot cover the fee
  So that I am never charged for a payment that did not go through

  Scenario: Wallet is Rs. 1 short of the total payable
    Given the driver "Hina" is registered and logged in
    And the driver has linked the petrol vehicle "XYZ-789"
    And the wallet balance is Rs. 239
    And the vehicle was parked for 130 minutes
    When the vehicle exits
    Then the message should be "Insufficient wallet balance"
    And the wallet balance should be Rs. 239
    And the exit gate should be closed
