from __future__ import annotations
import importlib.abc


import importlib
import importlib.resources
from pathlib import Path


from . import (
    _pythonize_name,
    _initialize_jinja,
    GlobalReference,
    pkg_resources,
)

from .. import CodeGenException

from ...core.schemaparse import (
    MetaSchemaSet,
)

from .module_generator import MetaschemaModuleGenerator

from .datatypes_generator import DatatypeModuleGenerator


#
# Classes to parse the metaschemaset
#


jinja_env = _initialize_jinja()


class PackageGenerator:
    """
    This class is initialized with a MetaSchemaSet and generates a package with Python source
    code for each of the metaschemas.
    """

    def __init__(
        self,
        parsed_metaschemas: MetaSchemaSet,
        destination_directory: Path,
        package_name: str,
        ignore_existing_files: bool = False,
    ) -> None:
        """
            This class is initialized with a MetaSchemaSet and generates a package with Python source
        code for each of the metaschemas.

            Args:
                parsed_metaschemas (MetaSchemaSet): The metaschemas parsed by the schemaparse module
                destination_directory (Path): The directory to write the generated code to
                package_name (str): the name of the package containing the modules
                ignore_existing_files (bool, optional): Whether to ignore existing directories and files. If true, will overwrite. If false will throw an exception. Defaults to False.
        """
        # initialize the package
        self.metaschema_set = parsed_metaschemas
        self.destination = destination_directory
        self.package_name = package_name
        self.module_generators: list[
            MetaschemaModuleGenerator | DatatypeModuleGenerator
        ] = []

        # generate code for all of the core datatypes
        self.generate_datatype_module()

        # collect all the elements of each metaschema which might be used across modules
        # and put them into a dictionary that can be passed to the module/class generators
        self.generate_global_reference_list()

        # generate modules for all of the schemas parsed.
        self.generate_schema_modules()

        # write the generated code to files in a directory.
        self.write_package(ignore_existing_files=ignore_existing_files)

    def generate_global_reference_list(self):
        """
        This function parses all of the metaschema global elements that each metaschema exports for reference in
        other schemas through "import". For each global element it creates a GlobalRef object with attributes
        that can be used to generate import statements in the python modules we generate. It also creates
        GlobalRef objects for datatypes since those are used by all modules.
        """
        self.global_refs: list[GlobalReference] = []
        for metaschema in self.metaschema_set.metaschemas:
            schema_source = str(metaschema.file)
            module_name = _pythonize_name(metaschema.short_name)
            for global_reference_key in metaschema.globals.keys():
                self.global_refs.append(
                    GlobalReference(
                        schema_source=schema_source,
                        module_name=module_name,
                        ref_name=_pythonize_name(global_reference_key),
                        class_name=_pythonize_name(
                            metaschema.globals[global_reference_key]
                        ),
                    )
                )

        # add references for metaschema datatypes, they look a little strange because
        # they're in the metaschema xsd, not a specific metaschema
        for datatype in self.metaschema_set.datatypes:
            if datatype.ref_name is not None:
                self.global_refs.append(
                    GlobalReference(
                        schema_source="datatype",
                        module_name="datatypes",
                        ref_name=_pythonize_name(datatype.ref_name),
                        class_name=_pythonize_name(datatype.name),
                    )
                )

    def generate_datatype_module(self):
        """
        Generates the module to represent the basic datatypes
        """
        self.module_generators.append(
            DatatypeModuleGenerator(datatypes=self.metaschema_set.datatypes)
        )

    def generate_schema_modules(self):
        """
        Generates a list of module to represent the metaschemas included in the metaschema set
        """
        for metaschema in self.metaschema_set.metaschemas:
            self.module_generators.append(
                MetaschemaModuleGenerator(
                    metaschema=metaschema,
                    global_refs=self.global_refs,
                )
            )

    def write_package(self, ignore_existing_files: bool) -> None:
        """
        Writes all the files in the package to files at a location provided.

        Note that we assume that thePath exists and represents an empty directory that can be written to.
        The caller is responsible for verifying that this is correct before giving us the path.
        We will raise Exceptions if anything doesn't work.
        """

        # check the destination directory.
        try:
            self._check_directory(self.destination, ignore_existing_files)
        except CodeGenException as e:
            raise CodeGenException(f"Error when checking destination directory: {e}")

        # create the directory Path by appending the provided base path and the provided package name
        package_path = Path(self.destination, self.package_name)

        package_path.mkdir(exist_ok=ignore_existing_files)

        # Get all of the package resource files
        for resource_file in importlib.resources.files(pkg_resources).iterdir():
            if resource_file.is_file() and resource_file.name.startswith("pkg."):
                self._copy_resource_file_to_pkg(resource_file, package_path)

        for module_generator in self.module_generators:
            module_file = package_path.joinpath(
                Path(f"{module_generator.module_name}.py")
            )
            module_file.write_text(module_generator.generated_module)

    def _copy_resource_file_to_pkg(
        self, resource_file: importlib.abc.Traversable, package_path
    ):
        # The file will be written to the package directory without the leading "pkg." in the filename
        target_filename = resource_file.name.lstrip("pkg.")
        with importlib.resources.as_file(resource_file) as r_file:
            package_path.joinpath(target_filename).write_text(r_file.read_text())

    def _check_directory(
        self, path_to_check: Path, ignore_existing_files: bool
    ) -> None:
        """
        Checks to make sure that a Path exists and represents and empty directory.
        Raises an exeption if this not true

        Args:
            path_to_check (Path): the Path to check.
        """
        if not path_to_check.exists():
            raise CodeGenException(f"{str(path_to_check)} does not exist.")

        if not path_to_check.is_dir():
            raise CodeGenException(
                f"{str(path_to_check)} exists but is not a directory."
            )

        if ignore_existing_files is False and len(list(path_to_check.iterdir())) > 0:
            raise CodeGenException(f"{str(path_to_check)} exists but is not empty.")
