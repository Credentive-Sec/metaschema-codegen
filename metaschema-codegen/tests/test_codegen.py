from metaschema_codegen.codegen.python.package_generator import (
    PackageGenerator,
    MetaschemaModelPackageGenerator,
    DatatypeModuleGenerator,
)

from metaschema_codegen.core.schemaparse import MetaSchemaSet


class TestPackageGenerator:
    def test_package_generator(self, generated_package: PackageGenerator):
        assert isinstance(
            generated_package,
            PackageGenerator,
        )

    def test_package_generator_contents(self, generated_package: PackageGenerator):
        assert generated_package.package_name is not None and isinstance(
            generated_package.package_name, str
        )

    def test_class_generator(self, generated_package: PackageGenerator):
        assert isinstance(generated_package.module_generators, list)

    def test_classes(self, generated_package: PackageGenerator):
        for m_gen in generated_package.module_generators:
            assert (isinstance(m_gen, MetaschemaModelPackageGenerator) 
                    or isinstance(m_gen, DatatypeModuleGenerator))


class TestDatatypesGenerator:
    def test_generate_datatypes(self, parsed_metaschema: MetaSchemaSet):
        dt_gen = DatatypeModuleGenerator(parsed_metaschema.datatypes)
        assert isinstance(dt_gen.generated_module, str)
