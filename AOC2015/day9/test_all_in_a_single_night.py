from all_in_a_single_night import Route, find_extreme_routes


def test_parse_route():
    text = "London to Dublin = 464"
    assert Route.parse(text) == Route("London", "Dublin", 464)


def test_find_extreme_routes():
    text = """London to Dublin = 464
    London to Belfast = 518
    Dublin to Belfast = 141"""
    routes = [Route.parse(route) for route in text.splitlines()]
    assert find_extreme_routes(routes) == (605, 982)
