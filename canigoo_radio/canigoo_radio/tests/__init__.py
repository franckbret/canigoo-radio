import datetime


def create_user(
        self, email="user@canigoo.test", username="bob", password="pop"):
    return self.registry.User.insert(
        email=email,
        username=username,
        password=password,
    )


def create_presenter(self, name="Dj Foo"):
    return self.registry.Presenter.insert(
        name=name,
    )


def create_show(self, name="FooBar radio show", presenter=None):
    return self.registry.Show.insert(
        name=name,
        presenter=presenter,
    )


def create_event(
        self, start=None, end=None, name="FooEvent #1", show=None):
    start = start or datetime.datetime.now()
    end = end or start + datetime.timedelta(hours=1)
    if not show:
        presenter = self.create_presenter()
        show = self.create_show(presenter=presenter)

    return self.registry.Event.insert(
        name=name,
        start=start,
        end=end,
        show=show
    )
