import argparse
class ArgsFromCMD(object):
    #: base class for other ways to make lights
    def __init__(self, description='Default description'):
        self.parser = argparse.ArgumentParser(description=description)
        self.description = description
        self.set_args()
        self.get_args()
        self.process_args()
        self.cleanup_parser()

    def get_args(self):
        args, unused_args = self.parser.parse_known_args()
        if unused_args is not None:
            msg = 'Warning! Parser described as {} Unused/unrecognized arguments: {}'.format(self.description, unused_args)
            print(msg)
        self.args = vars(args)
        
    def set_args(self):
        pass

    def process_args(self):
        pass
    
    def cleanup_parser(self):
        del self.parser
