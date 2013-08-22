from saml.schema import utils


class TestPascalize:

    def test_normal(self):
        text = 'something'

        assert utils.pascalize(text) == 'Something'

    def test_underscore(self):
        text = 'some_thing'

        assert utils.pascalize(text) == 'SomeThing'

    def test_already(self):
        text = 'someThing'

        assert utils.pascalize(text) == 'SomeThing'

    def test_dash(self):
        text = 'some-thing'

        assert utils.pascalize(text) == 'SomeThing'

    def test_null(self):
        text = 'SomeThing'

        assert utils.pascalize(text) == 'SomeThing'

    def test_pascal(self):
        text = 'Some_thing'

        assert utils.pascalize(text) == 'SomeThing'
