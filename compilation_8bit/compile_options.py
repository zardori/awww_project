class Option:

    def __init__(self, name, group, radio=True):
        self.name = name
        self.group = group
        self.radio = radio
        self.checked = False

    def __str__(self):
        return "Option(" + self.name + ", " + self.group + ", " + str(self.radio) + ", " \
            + str(self.checked)


class CompileOptions:

    def __init__(self):

        C11 = Option("C11", "standard")
        C98 = Option("C98", "standard")
        C89 = Option("C89", "standard")

        MCS51 = Option("MCS51", "architecture")
        Z80 = Option("Z80", "architecture")
        STM8 = Option("STM8", "architecture")

        self.standard = [
            Option("C89", "standard"),
            Option("C98", "standard"),
            Option("C11", "standard"),
        ]

        self.optimization = [
            Option("opt1", "aaa"),
            Option("opt2", "aaa"),
        ]

        self.architecture = [
            Option("MCS51", "architecture"),
            Option("Z80", "architecture"),
            Option("STM8", "architecture"),
        ]


        self.name_to_option_dict = {}

        for options_of_type in [self.standard, self.optimization, self.architecture]:
            for option in options_of_type:
                self.name_to_option_dict[option.name] = option


        options_dict = {

            "tab_1": {
                "option_group_1": ["option_1", "option_2"],
                "option_group_2": ["option_1", "option_2", "option_3"]
            },
            "tab_2": {
                "option_group_1": ["option_1"]
            },
            "tab_3": {

            },
            "tab_4": {
                "option_group_1": ["option_a", "option_b"]

            }

        }





    def name_to_opt(self, name):
        return self.name_to_option_dict[name]


compile_options = CompileOptions()
