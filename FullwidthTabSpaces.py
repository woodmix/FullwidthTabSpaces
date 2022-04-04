import sublime
import sublime_plugin

#===========================================================================================================
class FullwidthTabSpacesListener(sublime_plugin.ViewEventListener):
    """
    日本語文字を含む行でTabキーを押すと、ストップ位置がずれる問題に対応する。
    """

    #-----------------------------------------------------------------------------------------------------------
    def applies_to_primary_view_only():
        """
        複製されたビューでも動作するようにする。
        """
        return False

    #-----------------------------------------------------------------------------------------------------------
    def on_text_command(self, command_name, args):

        # 水平タブの insert コマンドが発行されたら独自コマンドに転送する。ただし、translate_tabs_to_spaces がONになっている場合に限る。
        if command_name == "insert" and args["characters"] == "\t" and self.view.settings().get("translate_tabs_to_spaces", False):
            return ("fullwidth_tab_spaces")


#===========================================================================================================
class FullwidthTabSpacesCommand(sublime_plugin.TextCommand):
    """
    キャレット位置に水平タブと同等幅のスペースを挿入するコマンド。
    """

    #-----------------------------------------------------------------------------------------------------------
    def run(self, edit):

        # 各選択領域を一つずつ処理する。
        for region in self.view.sel():
            self.processOne(region, edit)

    #-----------------------------------------------------------------------------------------------------------
    def processOne(self, region, edit):
        """
        指定された選択領域を処理する。
        """

        # 半角幅とインデントサイズを取得。
        em = self.view.em_width()
        size = self.view.settings().get("tab_size", 4)
        tabwid = em * size

        # 選択始端のX座標を取得。
        vec = self.view.text_to_layout( region.begin() )

        # 次のタブストップ位置までの距離を計算して、その位置までに必要な半角スペースの数を取得。
        dist = tabwid - vec[0] % tabwid
        num = round(dist / em)
        num = 4 if num <= 0 else num

        # その数のスペースを挿入するコマンドに置き換える。
        self.view.erase(edit, region)
        self.view.insert(edit, region.begin(), " "*num)


#===========================================================================================================
class FullwidthTabAlignCommand(sublime_plugin.TextCommand):
    """
    複数のキャレットの前方にスペースを挿入して、一番うしろに位置しているキャレット位置に合わせるコマンド。
    """

    #-----------------------------------------------------------------------------------------------------------
    def run(self, edit):

        # 各選択領域を一つずつ見て、行番号をキー、その行で最も前方にある選択領域を値とする dict を作成する。
        targets = {}
        for region in self.view.sel():

            row, _ = self.view.rowcol(region.b)

            if row not in targets:
                targets[row] = region

        # 作成した dict を一つずつ見て、最も後ろのキャレットＸ座標を取得。
        alignx = 0
        for region in targets.values():

            vec = self.view.text_to_layout(region.b)

            if alignx < vec[0]:
                alignx = vec[0]

        # dict にある各キャレットにスペースを挿入していき、最も後ろのＸ座標に合わせる。
        # 先頭から順次挿入していくと後続の選択領域は後ろにずれてtargetsで保持しているRegionと合わなくなるため、reversed() で末尾から処理する。
        for _, region in reversed(sorted(targets.items(), key=lambda p: p[0])):

            vec = self.view.text_to_layout(region.b)

            spaces = round( (alignx - vec[0]) / self.view.em_width() )

            self.view.insert(edit, region.b, " "*spaces)
