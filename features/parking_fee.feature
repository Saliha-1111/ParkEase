@boundary
Feature: Parking fee for petrol cars
  As a registered ParkEase driver
  I want the parking fee to follow the published tariff
  So that I know exactly what will be charged when I exit

  Background:
    Given the driver "Sara" is registered and logged in
    And the driver has linked the petrol vehicle "ABC-123"
    And the wallet balance is Rs. 5,000

  Scenario Outline: Fee for different parking durations
    Given the vehicle was parked for <minutes> minutes
    When the vehicle exits
    Then the parking fee should be Rs. <parking_fee>
    And the service charge should be Rs. <service_charge>
    And the total paid should be Rs. <total>

    Examples: Free and rounding
      | minutes | parking_fee | service_charge | total |
      | 10      | 0           | 0              | 0     |
      | 15      | 0           | 0              | 0     |
      | 16      | 100         | 20             | 120   |
      | 60      | 100         | 20             | 120   |
      | 61      | 160         | 20             | 180   |
      | 130     | 220         | 20             | 240   |

    Examples: Daily cap
      | minutes | parking_fee | service_charge | total |
      | 720     | 760         | 20             | 780   |
      | 721     | 800         | 20             | 820   |
      | 1200    | 800         | 20             | 820   |
