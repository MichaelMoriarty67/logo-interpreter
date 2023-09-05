import utils


class OuputException(Exception):
    def __init__(self, exp):
        self.exp = exp

    def get_exp(self):
        return self.exp


class UnboundVarError(Exception):
    def __init__(self, name):
        self.name = name


class Environment:
    def __init__(
        self,
        procedures: dict,
        vars: dict,
        base_env=None,
        name: str = None,
    ):
        self.procedures = procedures
        self.variables = vars
        self.base_env = base_env
        self.name = name

    def add_proc(self, proc_name, body, args=(), args_count=0, user_defined=True):
        """Adds or updates a name in the procedures dictionairy."""
        new_proc = Procedure(
            name=proc_name,
            args=args,
            body=body,
            user_defined=user_defined,
            args_count=args_count,
        )
        self.procedures[proc_name] = new_proc

    def add_var(self, name, value):
        """Adds or updates a name in the variables dictionairy."""
        e, _ = self.get_var(name)
        if e is not None:
            e.variables[name] = value
        else:
            g = utils.find_global_env(self)
            g.variables[name] = value

    def get_proc(self, name):
        """Returns the value bound to a specified name or None."""
        return self.procedures[name]

    def get_var(self, name):
        """Returns the value bound to a specified name and the env it's found in."""
        env = self
        value = None

        while env:
            try:
                value = self.variables[name]
                return env, value
            except UnboundLocalError and KeyError:
                env = env.base_env

        if value is None:
            raise UnboundVarError(name)

        return env, value

    def __repr__(
        self,
    ) -> str:  # this could be formatted cooler to show more like a receipt
        return f"""Environment: {self.name}
Current vars: {self.variables}
Current procedures: {self.procedures}"""


class Procedure:
    def __init__(
        self, name: str, args, body, user_defined: bool, args_count: int
    ) -> None:
        self.name = name
        self.body = body  # each line should be stored as a string, not a nested list
        self.args = args
        self.user_defined = user_defined
        self.args_count = args_count
