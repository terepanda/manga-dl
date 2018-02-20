from urllib.parse import unquote_plus

from src.providers.hentaifox_com import HentaiFoxCom


class HitomiLa(HentaiFoxCom):
    _idx_re = r'/(?:galleries|reader)/(\d+)'
    _url_str = '{}/galleries/{}.html'
    _name_re = '.dj-gallery h1 a'
    _cdn = 'http://0a.hitomi.la/galleries/'

    def get_manga_name(self):
        name = super().get_manga_name()
        return unquote_plus(name.split('|')[0].strip())

    def get_files(self):
        idx = self.re.search(self._idx_re, self.get_url()).group(1)
        url = 'http://ltn.hitomi.la/galleries/{}.js'.format(idx)
        images = self.re.search(r'(\[.+\])', self.http_get(url))
        images = self.json.loads(images.group(1))
        p = '{}{}/'.format(self._cdn, idx)
        return [p + i.get('name') for i in images]


main = HitomiLa
