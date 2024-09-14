# just in case, here is an example case that you can drop in and run to check on what this code is doing:
# class ExampleDummy():
#     children: dict
#     def __init__(self):
#         object.__setattr__(self, "children", {})
#     def _resolve_target(self, name):
#         if isinstance(self.children[name], list):
#             return self.children[name]
#         return [self.children[name]]
#     def __getattr__(self, name):
#         return self.children[name]
#     def __setattr__(self, name, value):
#         self.children[name] = value
# root = ExampleDummy()
# root.location = ExampleDummy()
# root.location.subelements = [ExampleDummy(), ExampleDummy(), ExampleDummy()]
# root.location.subelements[0].example = 3
# root.location.subelements[0].selector = 2
# root.location.subelements[1].example = 4
# root.location.subelements[1].selector = 3
# root.location.subelements[2].example = 5
# root.location.subelements[2].selector = 5

# mp = Metapath("location/subelements[selector > 2]/example")
# print(mp.eval(root)[0])
