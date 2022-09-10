from data import MENU, resources


def print_resources():
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g")
    print(f"Money: ${resources['money']}")


def make_payment():
    """
    Asks the user to insert the required coins and returns the total amount of money inserted
    """
    payment_details = {
        'quarters': 0,
        'dimes': 0,
        "nickles": 0,
        'pennies': 0,
    }

    total = 0
    for coin in payment_details:
        amount = int(input(f"How many {coin}? "))

        if coin == 'quarters':
            total += amount * 0.25
        elif coin == 'dimes':
            total += amount * 0.10
        elif coin == 'nickles':
            total += amount * 0.05
        elif coin == "pennies":
            total += amount * 0.01

    return total


def prepare_coffee(coffee):
    """
    Returns True if was able to prepare the coffee
    """
    print(f"Preparing your {coffee}")

    for ingredient in MENU[coffee]['ingredients']:
        amount = MENU[coffee]['ingredients'][ingredient]
        if resources[ingredient] < amount:
            print(f"There is not enough {ingredient} to prepare your coffee")
            return False

        resources[ingredient] -= amount

    resources['money'] += MENU[coffee]['cost']

    return True


def reset_machine(coffee):
    """
    If the machine wasn't able to prepare the coffee because of lack of ingredients it replenishes the ingredients used
    """
    for ingredient in MENU[coffee]['ingredients']:
        amount = MENU[coffee]['ingredients'][ingredient]
        if resources[ingredient] >= amount:
            resources[ingredient] += amount
        else:
            return


def give_change(total, cost):
    """
    If the user pays more than the actual cost it calculates and return the user his/her change
    """
    print("Calculating your change")
    change_details = {
        'quarters': 0,
        'dimes': 0,
        "nickles": 0,
        'pennies': 0,
    }

    total_change = total - cost

    change = f"Your change is: ${total_change:.2} you are given: "
    for coin in change_details:
        if coin == 'quarters':
            coin_value = 0.25
        elif coin == 'dimes':
            coin_value = 0.10
        elif coin == 'nickles':
            coin_value = 0.05
        elif coin == 'pennies':
            coin_value = 0.01
        else:
            coin_value = 0

        if total_change > 0:
            change_details[coin] = total_change // coin_value
            change += f" {change_details[coin]} {coin} "
            total_change -= change_details[coin] * coin_value

    print(change)


machine_status = True
while machine_status:
    action = input("What would you like? (espresso, latte, cappuccino) ").lower()

    if action == "off":
        print("Turning the machine off")
        machine_status = False
    elif action == "report":
        print_resources()
    else:
        if action in MENU:
            selected_menu = MENU[action]
            print(f"{action} costs: ${selected_menu['cost']}")
            print("Please insert coins...")

            total_payed = make_payment()

            if total_payed < selected_menu['cost']:
                print(f"You payed {total_payed}. Sorry that is not enough money. Money refunded")
            elif total_payed > selected_menu['cost']:
                give_change(total_payed, selected_menu['cost'])

            if not prepare_coffee(action):
                reset_machine(action)
            else:
                print(f"Here is your {action} ☕ Enjoy!")
        else:
            print("Select one of the options")
