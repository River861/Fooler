from pathlib import Path
import shutil
import json


class ColonyGenerator(object):

    def __init__(self, config):
        self.__start_path = config['start_path']
        self.__opening = config['opening']
        self.__levels = config['levels']
        self.__conclusion = config['conclusion']

    def generate(self):
        stage_path = Path(self.__start_path)
        for msg in self.__opening:
            stage_path = self.__add_channel(stage_path, msg)
        for level in self.__levels:
            question, options, depth, answer, traps = tuple(level.values())
            stage_path = self.__add_channel(stage_path, question)
            self.__add_tree(stage_path, options, depth)
            self.__add_bombs(stage_path, traps)
            stage_path = self.__add_channel(self.__add_exit(stage_path, answer), "Stage Clear!")
        for msg in self.__conclusion:
            stage_path = self.__add_channel(stage_path, msg)
        self.__add_treasure(stage_path)

    def __add_exit(self, root_path, psw):
        exit_path = Path(root_path)
        for step in psw:
            exit_path /= step
        exit_path.mkdir(exist_ok=True, parents=True)
        return exit_path

    def __add_bombs(self, root_path, wrong_psws):
        for wrong_psw in wrong_psws:
            ans, msg = tuple(wrong_psw.values())
            path = Path(root_path)
            for step in ans:
                path /= step
            if isinstance(msg, str):
                msg = [msg]
            for step in msg:
                path /= step
            path.mkdir(exist_ok=True, parents=True)

    def __add_channel(self, root_path, channel_msg):
        path = Path(root_path) / channel_msg
        path.mkdir(exist_ok=True, parents=True)
        return path

    def __add_tree(self, root_path, branches, depth):
        if not depth:
            return
        for branch in branches:
            path = Path(root_path) / branch
            path.mkdir(exist_ok=True)
            self.__add_tree(path, branches, depth-1)

    def __add_treasure(self, dst_path):
        for fn in Path(".").glob("*"):
            if(fn.is_dir()):
                continue
            shutil.copy(str(fn), str(dst_path))


if __name__ == '__main__':
    with Path('config.json').open(mode='r') as f:
        config = json.load(f)
        cg = ColonyGenerator(config)
        cg.generate()
