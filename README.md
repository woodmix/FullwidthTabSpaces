# FullwidthTabSpaces (en)

Sublime Text has a setting called translate_tabs_to_spaces which, if set to true, will cause horizontal tabs to be inserted using space characters.
However, since the tab stop position is calculated based on the number of characters only, the stop position will be shifted if the line contains full-width characters in front. This plugin compensates for this problem.

However, it assumes monospaced fonts. If you are using a proportional font, it is not recommended because the space characters inserted by horizontal tabs will be inconsistent.

Internally, it works by intercepting the command ("insert", {"characters":"\t"}), so no special configuration is required, just install it and it will work.
If you want to turn off the feature, disable it or uninstall it.

It only works if translate_tabs_to_spaces is set to true.

In addition, it includes a command to align digits by inserting a space in front of multiple carets. You can use it by setting Preferences => Key Bindings to `{ "keys": ["ctrl+alt+a"], "command": "fullwidth_tab_align" },` and so on.

\* I don't have a Mac, so it has not been tested on a Mac.

Translated with www.DeepL.com/Translator (free version)

# FullwidthTabSpaces (ja)

Sublime Text には translate_tabs_to_spaces という設定項目があって、trueにすると水平タブがスペース文字を使って挿入されるようになります。
しかし、単純に字数のみでタブストップ位置を計算しているため、前方に全角文字を含む行ではストップ位置がずれます。このプラグインはこの問題を補正します。

ただし等幅フォントを前提としています。プロポーショナルフォントをお使いの場合は水平タブで挿入されるスペース文字列が一定しなくなるので、オススメしません。

内部的には ("insert", {"characters": "\t"}) のコマンドをインターセプトして動作しますので、特に設定は不要です。インストールするだけで効果を発揮します。
機能をオフにしたい場合は無効化するかアンインストールして下さい。

機能が働くのは translate_tabs_to_spaces がtrueになっている場合のみです。falseの場合は何もしません。

ついでに、複数のキャレットの前方にスペースを挿入して桁位置を合わせるコマンドも入っています。
Preferences => Key Bindings で `{ "keys": ["ctrl+alt+a"], "command": "fullwidth_tab_align" },` などと設定していただくことで使用できます。

※私はMacを所持していませんので、Macでの動作確認は行われていません。
