import elementpath

class TestTDOP:
    def test_parse_to_selector(self, metapaths: list[str]):
        for metapath in metapaths:
            path_selector = elementpath.Selector(metapath)
            assert isinstance(
                path_selector,
                elementpath.Selector
            )