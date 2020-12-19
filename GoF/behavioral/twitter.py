from GoF.behavioral.Observer import Observer, Observable


class Twitter(Observable, Observer):

    def __init__(self, nickname):
        super().__init__()
        self._nickname = nickname

    @property
    def nickname(self):
        return self._nickname

    def update(self, subscription):
        print(f'{self.nickname} likes {subscription.nickname}\'s post!')

    def follow(self, subscription):
        subscription.add_observer(self)
        return self

    def unfollow(self, subscription):
        subscription.delete_observer(self)

    def tweet(self, text):
        print(f'{self.nickname} says: {text}')
        super().notify_observers()


def go_do_twitter():
    a = Twitter('Alice')
    k = Twitter('King')
    q = Twitter('Queen')
    h = Twitter('Mad Hatter')
    c = Twitter('Cheshire Cat')

    a.follow(c).follow(h).follow(q)
    k.follow(q)
    q.follow(q).follow(h)
    h.follow(a).follow(q).follow(c)

    q.tweet('Off with their heads!\n')
    a.tweet('What a strange world we live in!\n')
    k.tweet('Begin at the beginning, and go on until you come to the end: then stop.\n')


if __name__ == "__main__":
    go_do_twitter()
