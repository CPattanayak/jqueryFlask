Feature: UI Functional Flow

    Scenario Outline: Order management senario
        Given For given user "<user_name>" ph "<phone>" quantity "<qty>"
        When when placing order
        Then reciving success alert
        When when move to admin page
        Then check verify edit alert
        When delete button click
        Then displaying no data found
        Examples:
          | user_name | phone   |  qty |
          |  abc      | 99999999 | 20   |
          |  xyz      | 35555555 | 30    |
          |  aaa      | 88888888 | 50    |
