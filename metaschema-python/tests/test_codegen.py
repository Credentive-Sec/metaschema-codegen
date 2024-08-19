from metaschema_python.codegen.python.codegen import (
    PackageGenerator,
    MetaschemaModuleGenerator,
    DatatypeModuleGenerator,
    SimpleDatatypeClassGenerator,
)


class TestPackageGenerator:
    def test_package_generator(self, generated_package):
        assert isinstance(
            generated_package,
            PackageGenerator,
        )

    def test_package_generator_contents(self, generated_package):
        assert generated_package.package_name is not None and isinstance(
            generated_package.package_name, str
        )

    def test_class_generator(self, generated_package):
        assert isinstance(generated_package.module_generators, list)

    def test_classes(self, generated_package):
        for m_gen in generated_package.module_generators:
            assert isinstance(m_gen, MetaschemaModuleGenerator) or isinstance(
                m_gen, DatatypeModuleGenerator
            )


class TestDatatypesGenerator:
    def test_generate_datatypes(self, parsed_metaschema):
        dt_gen = DatatypeModuleGenerator(parsed_metaschema.datatypes)
        assert isinstance(dt_gen.generated_module, str)
