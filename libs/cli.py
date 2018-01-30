import sys
from argparse import ArgumentParser
from os import name as os_name

from progressbar import ProgressBar

from libs.parser import Parser
from libs.version import __version__

__downloader_uri__ = 'https://github.com/yuru-yuri/manga-dl'


def get_cli_arguments() -> ArgumentParser:  # pragma: no cover
    args_parser = ArgumentParser()

    args_parser.add_argument('-v', '--version', action='version', version=__version__)

    args_parser.add_argument('-u', '--url', type=str, required=False, help='Downloaded url', default='')
    args_parser.add_argument('-n', '--name', type=str, required=False, help='Manga name', default='')
    args_parser.add_argument('-d', '--destination', type=str, required=False,
                             help='Destination folder (Default = current directory', default='')
    args_parser.add_argument('-i', '--info', action='store_const', required=False, const=True, default=False)
    args_parser.add_argument('-np', '--no-progress', action='store_const', required=False, const=True,
                             help='Don\'t how progress bar', default=False)
    args_parser.add_argument('-s', '--skip-volumes', type=int, required=False, help='Skip volumes (count)', default=0)
    args_parser.add_argument('-c', '--max-volumes', type=int, required=False,
                             help='Maximum volumes for downloading 0=All (count)', default=0)
    args_parser.add_argument('--user-agent', required=False, type=str, help='Don\'t work from protected sites',
                             default='')
    args_parser.add_argument('--proxy', required=False, type=str, help='Http proxy', default='')

    args_parser.add_argument('--no-name', action='store_const', required=False,
                             help='Don\'t added manga name to the path', const=True, default=False)
    args_parser.add_argument('--disallow-webp', action='store_const', required=False, help='Allow downloading webp images',
                             const=True, default=False)
    args_parser.add_argument('--force-png', action='store_const', required=False,
                             help='Force conversation images to png format', const=True, default=False)
    args_parser.add_argument('--reverse-downloading', action='store_const', required=False,
                             help='Reverse volumes downloading', const=True, default=False)
    args_parser.add_argument('--rewrite-exists-archives', action='store_const', required=False, const=True,
                             default=False)
    args_parser.add_argument('-nm', '--no-multi-threads', action='store_const', required=False,
                             help='Disallow multi-threads images downloading', const=True, default=False)
    args_parser.add_argument('-xt', required=False, type=int, help='Manual image crop with top side', default=0)
    args_parser.add_argument('-xr', required=False, type=int, help='Manual image crop with right side', default=0)
    args_parser.add_argument('-xb', required=False, type=int, help='Manual image crop with bottom side', default=0)
    args_parser.add_argument('-xl', required=False, type=int, help='Manual image crop with left side', default=0)

    args_parser.add_argument('--crop-blank', action='store_const', required=False, help='Crop white lines on image',
                             const=True, default=False)
    args_parser.add_argument('--crop-blank-factor', required=False, type=int, help='Find factor 0..255. Default: 100',
                             default=100)
    args_parser.add_argument('--crop-blank-max-size', required=False, type=int,
                             help='Maximum crop size (px). Default: 30', default=30)

    args_parser.add_argument('--cli', action='store_const', required=False, const=True, help='Use cli interface',
                             default=False)

    # future
    args_parser.add_argument('--server', action='store_const', required=False, const=True, help='Run web interface',
                             default=False)

    return args_parser


class Cli:
    status = True
    args = None
    parser = None
    __progress_bar = None

    def __init__(self, args: ArgumentParser):
        self.args = args.parse_args()
        self.parser = Parser(args)

    def start(self):
        self.parser.init_provider(
            progress_callback=self.progress,
            logger_callback=self.print,
            quest_callback=self.quest,
        )
        self.parser.start()

    def input(self, prompt: str = ''):
        return input(prompt=prompt + '\n')

    def __init_progress(self, items_count: int, re_init: bool):
        if re_init or not self.__progress_bar:
            bar = ProgressBar()
            self.__progress_bar = bar(range(items_count))
            self.__progress_bar.init()

    def progress(self, items_count: int, current_item: int, re_init: bool = False):
        if not items_count:
            return
        if not self.args.no_progress:
            self.__init_progress(items_count, re_init)
            self.__progress_bar.update(current_item)

    def print(self, text, end='\n'):
        if os_name == 'nt':
            text = str(text).encode().decode(sys.stdout.encoding, 'ignore')
        print(text, end=end)

    def _single_quest(self, variants, title):
        self.print(title)
        for v in variants:
            self.print(v)
        return self.input()

    def _multiple_quest(self, variants, title):
        self.print('Accept - blank line + enter')
        self.print(title)
        for v in variants:
            self.print(v)
        result = []
        while True:
            _ = self.input().strip()
            if not len(_):
                return result
            result.append(_)

    def quest(self, variants: enumerate, title: str, select_type=0):  # 0 = single, 1 = multiple
        if select_type:
            return self._multiple_quest(variants, title)
        return self._single_quest(variants, title)
