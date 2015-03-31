import re

class Puki2Redmine:
    p2r = { '*': '#', '-': '*'}

    def __init__(self, text):
        self.puki_text = text

    def clean_up(self):
        """
        Remove titile color like '[#q6f4c53e]'
        and break '~'
        """
        new_text = []
        for line in self.puki_text:
            if line:
                cline = line.strip()
                r = re.sub('(\[.*\])', '', cline)
                if len(r) > 1:
                    if r[-1] == '~':
                        r = r[:-1]
                new_text.append(r)
            else:
                new_text.append('')
        self.puki_text = new_text

    def replace_markdown(self):
        """
        Replace pukiwiki markdown to markdown
        """

        new_text = []
        for line in self.puki_text:
            if line:
                r = self._replace_markdown_imp(line)
                new_text.append(r)
            else:
                new_text.append('')
        self.puki_text = new_text

    def _replace_markdown_imp(self, line):
        """
        Implimentation of repalce markdown
        """
        kome_reg = re.compile('^\*+')
        dash_reg = re.compile('^-+')
        plus_reg = re.compile('^\++')

        def replace_f(reg, symbol, line):
            it = reg.finditer(line)
            if it:
                for m in it:
                    nl = reg.sub('', line)
                    r = symbol * m.span()[1] + ' ' + nl
                    return r
        r = replace_f(kome_reg, '#', line)
        if r:
            return r
        r = replace_f(dash_reg, '*', line)
        if r:
            return r
        r = replace_f(plus_reg, '1.', line)
        if r:
            return r
        return line

    def convert(self):
        """
        Convert pukiwiki format to Markdown
        """
        self.clean_up()
        self.replace_markdown()
        return self.puki_text

if __name__ == "__main__":
    text = """\
**DNS [#v07205fd]
-IPとホスト名の対応を教えてくれるサービス
-ホスト名からIPを引けるようにする場合(正引き)
以下、Weigelaで上がっている仮想マシン（2014/3情報）~
+GREEN_SFC_K2~
 ドメイン登録されていない
 vi /var/named/named.hosts
"""
    p2r = Puki2Redmine(text.splitlines())
    r = p2r.convert()
    print("\n".join(r))


