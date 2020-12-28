import GoF.behavioral.Chain.ChainOfATM as Chn


class ATMProxyGuard(Chn.ATMInterface):

    def __init__(self, atm: Chn.ATM):
        self.__atm = atm
        self.__history: tuple = tuple()

    # Помимо всего прочего...
    # А если бы таких проверок было много, то получился бы опять Чейн :)
    def cash_out(self, amount: int):

        # Оригинальный банкомат не поддерживает проверки, это задача для прокси.
        if self.__atm.total() < amount:
            print('Not enough money. Please try entering less.')
        else:
            if all([amount % banknote for banknote in self.available()]):
                print(f'Sorry, wrong sum. Don\'t have bills to give out. Available: ')
                print(*self.available(), sep='      ')
            else:
                # При кэшауте последний снимок банкнот теряет смысл
                self.__history = tuple()
                self.__atm.cash_out(amount)
                print()

    # Пересчет доступных банкнот запрашивается только если были произведены какие-то операции. Иначе - из истории.
    def available(self) -> tuple:
        if not self.__history:
            self.__history = self.__atm.available()
        else:
            print('This message is printed when the proxy imitates the real atm.')
        return self.__history


def demo():

    modules = [Chn.Module(i, 20) for i in [500, 200, 100, 50]]
    modules[0].then(modules[1]).then(modules[2]).then(modules[3])

    atm = Chn.ATM(modules)
    atm_proxy = ATMProxyGuard(atm)

    atm_proxy.cash_out(120)
    atm_proxy.cash_out(5000)
    atm_proxy.cash_out(3250)
    atm_proxy.cash_out(7400)
    atm_proxy.cash_out(5750)
    atm_proxy.cash_out(400)

    h1 = atm_proxy.available()
    h2 = atm_proxy.available()
    print('Were last two results the same object? ' + str(h1 == h2))


if __name__ == "__main__":

    demo()
