import utils

class Environment:
    def __init__(self, procedures, vars, base_env = None, name = None ):
        self.procedures = procedures
        self.variables = vars
        self.base_env = base_env
        self.name = name
    
    def add_proc(self, name, value, args = (), args_count = 0, user_defined = True):
        """Adds or updates a name in the procedures dictionairy."""
        proc = Procedure(
            name,
            args,
            value,
            user_defined,
            args_count
        )
        self.procedures[name] = proc

    def add_var(self, name, value):
        """Adds or updates a name in the variables dictionairy."""
        e, _ = self.get_var(name)
        if e is not None:
            e.variables[name] = value
        else:
            g = utils.find_global_env(self)
            g.variables[name] = value

    def rem_name(self, name):
        """Removes a name in the values dictionairy."""
        pass
    
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
        return env, value


    def __repr__(self) -> str: # this could be formatted cooler to show more like a receipt
        return """Environment: {}
        
        Varibale Dictionary:
        _________
        {}
        
        """.format(self.name, self.variables)
    


class Procedure:
    def __init__(self, name, args, body, user_defined, args_count) -> None:
        self.name = name
        self.body = body
        self.args = args
        self.user_defined = user_defined
        self.args_count = args_count