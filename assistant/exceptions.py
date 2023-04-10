class FailedIKINE(Exception):
    def __init__(self, ikine_obj):
        self.ikine_obj = ikine_obj
        self.message = f"IKINE operation has failed at {ikine_obj.iterations}" \
                       f" iterations with a resulting q={ikine_obj.q}"
        super().__init__(self.message)
