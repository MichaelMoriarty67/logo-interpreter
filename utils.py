def str_friendly_unpack(*args,):
        """Unpacks all args into a single list, in order, without deconstructing any string iterables."""
        l = []
        for i in range(len(args)):
            if type(args[i]).__name__ == "str":
                l.append(args[i])
            else:
                for item in args[i]:
                    l.append(item)
                # l.append(*args[i])

        return l