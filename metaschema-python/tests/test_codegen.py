from metaschema_python.codegen.generate_classes import PackageGenerator


class TestPackageGenerator:
    def test_package_generator(self, generated_package):
        assert isinstance(
            generated_package,
            PackageGenerator,
        )

    def test_package_generator_contents(self, generated_package):
        assert generated_package.package is not None
