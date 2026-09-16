from spamoji import spamoji_class, spamoji_function


@spamoji_class("🎁")
class Present:
    @spamoji_function("✨")
    def __init__(self, contents: object):
        self.contents = contents

    @spamoji_function("🎉")
    def unwrap(self) -> object:
        return self.contents
