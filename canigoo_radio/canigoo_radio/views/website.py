from pyramid.view import view_config 


@view_config(route_name='homepage', renderer='../templates/home.jinja2')
def homepage(request):
    registry = request.anyblok.registry
    model = registry.get('Model.Event')
    title = "Canigoo radio station - Hi-Fidelity Music from the Center of the World!"
    current = model.get_current()
    if current:
        return dict(name=current.name,
                    show=current.show.name,
                    presenter=current.show.presenter.name,
                    title=title)
    else:
        return dict(show="Random memories are made of this!",
                    name="",
                    presenter="Canigoo Bot! 🤖",
                    title=title)
