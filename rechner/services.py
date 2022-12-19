from rechner.models import Address, ArbitrationBoard


def find_board(address: Address) -> ArbitrationBoard:
    raise NotImplementedError("This needs to be implemented")


def calculate_rent_increase(address, last_rent, last_rent_date, new_date) -> float:
    # TODO: Implement
    board = find_board(address)

    raise NotImplementedError("This needs to be implemented")
