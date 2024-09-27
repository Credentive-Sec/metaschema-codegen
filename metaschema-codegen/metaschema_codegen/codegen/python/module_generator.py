import typing

from ...core.schemaparse import Metaschema

from . import (
    _pythonize_name,
    _initialize_jinja,
    GlobalReference,
    GeneratedClass,
    ImportItem,
)

from . import flag_generator

jinja_env = _initialize_jinja()


class MetaschemaModuleGenerator:
    """
    A class to generate a python source code file (module) from a parsed metaschema. It will contain a class for
    every instance in the metaschema. It converts a data object representing a generic metaschema to a python
    oriented dictionary to pass to a template.
    """

    def __init__(
        self, metaschema: Metaschema, global_refs: list[GlobalReference]
    ) -> None:
        self.metaschema = metaschema
        self.version = typing.cast(str, metaschema.schema_dict["schema-version"])
        self.module_name = _pythonize_name(
            typing.cast(str, metaschema.schema_dict["short-name"])
        )
        self.generated_classes: list[GeneratedClass] = []

        #
        # The first pass is to generate the list of elements imported by or defined in the metaschema so that we can
        # identify the appropriate class for a "@ref". Not all of these refs are actually used by the module
        #
        # The format of the module import will be
        # from . import <module-name>
        # <...>
        # @dataclass
        # def Class:
        #     <ref_name>: <module-name>.<class-name>

        # get a list of elements from imports that could be referenced with a "@ref" in this module
        # The form will be {@ref: module.Class}
        imported_modules: list[str] = []
        module_refs: dict[str, str] = {}

        # Add all the refs from datatypes, since most of these will be used. Datatypes are not explicitly imported by a metaschem spec
        imported_modules.append("datatypes")
        module_refs.update(
            {
                global_ref.ref_name: f"{global_ref.class_name}"
                for global_ref in global_refs
                if global_ref.schema_source == "datatype"
            }
        )

        # get the list of explicitly imported schemas and add all the relevant global refs
        for schema in self.metaschema.imports:
            imported_modules.extend(
                [
                    global_ref.module_name
                    for global_ref in global_refs
                    if global_ref.schema_source == schema
                ]
            )
            module_refs.update(
                {
                    global_ref.ref_name: f"{global_ref.class_name}"
                    for global_ref in global_refs
                    if global_ref.schema_source == schema
                }
            )

        # record all of the top-level assemblies, flags and fields in this metaschema to include as local refs
        # Note that a locally defined instance's @ref will overwrite an import @ref, which I think is the correct behavior

        for flag in self.metaschema.schema_dict.get("define-flag", []):
            module_refs[f'{_pythonize_name(flag["@name"])}'] = (
                f'{_pythonize_name(flag["formal-name"])}'
            )

        for field in self.metaschema.schema_dict.get("define-field", []):
            module_refs[f'{_pythonize_name(field["@name"])}'] = (
                f'{_pythonize_name(field["formal-name"])}'
            )

        for assembly in self.metaschema.schema_dict.get("define-assembly", []):
            module_refs[f'{_pythonize_name(assembly["@name"])}'] = (
                f'{_pythonize_name(assembly["formal-name"])}'
            )

        #
        # Second Pass: With our ref dictionary in place, we perform a deeper parse to actually generate the classes.
        #

        for flag in self.metaschema.schema_dict.get("define-flag", []):
            self.generated_classes.append(
                flag_generator.TopLevelFlagClassGenerator(
                    class_dict=flag, refs=module_refs
                ).generated_class
            )

        # for field in self.metaschema.schema_dict.get("define-field", []):
        #     self.generated_classes.append(
        #         FieldClassGenerator(class_dict=field, refs=module_refs).generated_class
        #     )

        # With the classes generated, we create a dict to represent all of the actually used modules and classes
        imports = self._merge_imports(
            [g_class.refs for g_class in self.generated_classes]
        )

        # Finally, we are ready to generate the module source
        template_context = {}
        template_context["imports"] = imports
        template_context["classes"] = [
            generated_class.code for generated_class in self.generated_classes
        ]

        template = jinja_env.get_template("module.py.jinja2")

        self.generated_module = template.render(template_context)

    def _merge_imports(
        self, import_item_lists: list[list[ImportItem]]
    ) -> list[ImportItem]:
        # Take a list of ImportItems with redundant module/class parings
        # and produce a list of rationalized importItems
        merged_import_items = []

        import_dict: dict[str, list[str]] = {}  # create a dict for temp storage
        for import_item_list in import_item_lists:
            import_modules = [import_item.module for import_item in import_item_list]

            for module in import_modules:
                # Create import_dict entry if it doesn't exist
                if module not in import_dict.keys():
                    import_dict[module] = []

                import_dict[module].extend(
                    *[
                        import_item.classes
                        for import_item in import_item_list
                        if import_item.module == module
                    ]
                )

        # Convert import dict into list of ImportItems
        for module in import_dict.keys():
            merged_import_items.append(
                ImportItem(
                    module=module,
                    classes=set(
                        import_dict[module],
                    ),
                )
            )

        return merged_import_items
