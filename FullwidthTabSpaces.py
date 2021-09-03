import sublime
import sublime_plugin

#===========================================================================================================
class FullwidthTabSpacesListener(sublime_plugin.ViewEventListener):
    """
    日本語文字を含む行でTabキーを押すと、ストップ位置がずれる問題に対応する。
    """

    #-----------------------------------------------------------------------------------------------------------
    def on_text_command(self, command_name, args):

        # 水平タブの insert コマンドが発行されたら独自コマンドに転送する。ただし、translate_tabs_to_spaces がONになっている場合に限る。
        if command_name == "insert" and args["characters"] == "\t" and self.view.settings().get("translate_tabs_to_spaces", False):
            return ("fullwidth_tab_spaces")


#===========================================================================================================
class FullwidthTabSpacesCommand(sublime_plugin.TextCommand):
    """
    キャレット位置に水平タブと同等幅のスペースを挿入する
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
