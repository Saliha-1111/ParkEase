@smoke
Feature: Automatic wallet payment on exit
  As a registered ParkEase driver
  I want my parking fee to be charged automatically from my wallet when I exit
  So that I can leave the plaza without queuing at a payment booth

  Scenario: Registered EV driver pays after 3 hours 40 minutes
    Given the driver "Ali" is registered and logged in
    And the driver has linked the electric vehicle "LEA-1234"
    And the wallet balance is Rs. 1,000
    And the vehicle entered the plaza at 09:00
    When the vehicle exits at 12:40
    Then the message should be "Payment successful – gate opening"
    And the parking fee should be Rs. 280
    And the EV discount should be Rs. 70
    And the service charge should be Rs. 20
    And the total paid should be Rs. 230
    And the wallet balance should be Rs. 770
    And the exit gate should be open
