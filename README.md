# Redmine用リマインダー to slack
Redmineの期日が迫った投稿をslackに投げてあげる  
なんか要望があったので作って見た  
Python2.7でしか動作確認していない
## 前準備
* pipあたりでrequestsとpython-redmineを入れてあげる  
aptでもいいよ
* slackにIncoming Webhooksを入れてあげる
* RedmineのAPIを有効にする。ついでにAPI KEYも持ってくる
* default.pyをconfig.pyにコピーする  
config.pyの中身を設定する
## オプション
* --list_project  
プロジェクト一覧を表示  
projectsオプションで指定する時のIDを見たいときに使う
* --list_tracker  
トラッカー一覧を表示  
trackerオプションで指定する時のIDを見たいときに使う
* --projects PROJECTS
プロジェクトIDの指定。複数指定可(たぶん)  
指定しないと全プロジェクト
* --redmineurl REDMINEURL  
RedmineのURLを指定
* --redminekey REDMINEKEY  
Redmine のAPI Keyを指定
* --days DAYS  
期日までの日数  
7を指定すると*6日以下*のが表示される  
ちょっとおかしい気がするので変更するかも
* --tracker TRACKER  
指定トラッカーのみ表示
* --ignore_nodate  
期日未設定を表示しない
* --channel CHANNEL  
slackへの投稿チャンネル
* --username USERNAME  
slackへの投稿時ユーザ名
## 使い方
config.pyを適切に設定してあれば実行するだけ  
cronでやるといいんでない？
## 予定
* Python3に対応したい
* エラー処理をまともにしたい…けど、slack落ちたときでないと難しそう
* slack投稿時の書式を指定出来るようにしたい  
どういう指定方法がいいんだろう？
* Redmineのplugin(ruby)へは…やらない、かな

