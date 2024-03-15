import decimal


class ExchangeService:

    @classmethod
    def buy_from_exchange(cls, currency_name: str, amount: decimal.Decimal):
        print(f"Buying {amount} of {currency_name}")
        return True
