#!/usr/bin/env python
# vim: set ts=4 sw=4 et smartindent ignorecase fileencoding=utf8:
import argparse
import datetime
import json
import requests

# https://python-redmine.com/resources/project.html
# https://python-redmine.com/introduction.html
from redminelib import Redmine
from config import *

def post_slack(issues, username, channel):
    # 'assigned_to': 担当者
    # 'attachments': 添付ファイル
    # 'author': 編集者
    # 'changesets': 
    # 'children':
    # 'created_on': 作成日時
    # 'description': 詳細
    # 'done_ratio': 進捗率
    # 'due_date': 期日
    # 'id': ID
    # 'journals',
    # 'priority': 優先度
    # 'project': プロジェクト
    # 'relations',
    # 'start_date': 開始日
    # 'status': 状態
    # 'subject': タイトル
    # 'time_entries',
    # 'tracker': トラッカー
    # 'updated_on': 更新日
    # 'watchers': ウォッチ
    keys = issues.keys()
    keys.sort()
    body = []
    for key in keys:
        v = issues[key]
        vkey = dir(v)
        if 'due_date' in vkey:
            due_date = v.due_date.strftime('%Y/%m/%d')
        else:
            due_date = u'未設定'
        fields = []
        fields.append(dict(title = 'Limit', value = due_date, short = True))
        if 'assigned_to' in vkey:
            assigned_name = v.assigned_to.name
        else:
            assigned_name = u'担当者なし'
        fields.append(dict(title = 'Assign', value = assigned_name, short = True))

        url = REDMINE_URL + '/issues/{0}'.format(v.id)
        t = dict(title = v.subject, title_link = url, color = 'danger', fields = fields)
        body.append(t)

    payload = dict(
        channel = channel,
        username = username,
        icon_emoji = SLACK_EMOJI,
        attachments = body,
    )

    rslt = requests.post(SLACK_URL, data = json.dumps(payload))
    if rslt.status_code != requests.codes.ok:
        print(rslt.text)

def get_issues(projects, days, tracker, ignore_nodate):
    rslt = {}
    for v in projects.issues:
        if tracker and v.tracker.id != tracker:
            continue
        if 'due_date' in dir(v): # has_keyがない
            # 期日が設定されている
            due_date = v.due_date
            diff_days = (due_date - datetime.date.today()).days
        else:
            # 期日が設定されていない
            if ignore_nodate:
                continue
            diff_days = 0
        if diff_days < days:
            rslt[v.id] = v
    return rslt

def list_project(redmine):
    # ソートされていないのでソートして出したい
    rslt = []
    for v in redmine.project.all():
        rslt.append((v.id, v.name))
    rslt.sort()
    for v in rslt:
        print(u'{0}: {1}'.format(v[0], v[1]))

def list_tracker(redmine):
    rslt = []
    for v in redmine.tracker.all():
        rslt.append((v.id, v.name))
    rslt.sort()
    for v in rslt:
        print(u'{0}: {1}'.format(v[0], v[1]))

def parse_option():
    parser = argparse.ArgumentParser(description = u'redmine issues reminder to slack')
    parser.add_argument('--list_project', action = 'store_true', help = u'プロジェクト一覧を表示')
    parser.add_argument('--list_tracker', action = 'store_true', help = u'トラッカー一覧を表示')
    parser.add_argument('--projects', action = 'append', type = int, default = PROJECT_ID, help = u'project id')
    parser.add_argument('--redmineurl', type = str, default = REDMINE_URL, help = u'redmine web url')
    parser.add_argument('--redminekey', type = str, default = REDMINE_KEY, help = u'redmine api key')
    parser.add_argument('--days', type = int, default = REDMINE_DAYS, help = u'期日までの日数')
    parser.add_argument('--tracker', type = int, default = TRACKER_ID, help = u'指定トラッカーのみ表示')
    parser.add_argument('--ignore_nodate', action = 'store_true', help = u'期日未設定を表示しない')
    parser.add_argument('--channel', type = str, default = SLACK_CHANNEL, help = u'投稿チャンネル')
    parser.add_argument('--username', type = str, default = SLACK_USERNAME, help = u'slackユーザ名')
    return parser.parse_args()

def main():
    args = parse_option()

    redmine = Redmine(args.redmineurl, key = args.redminekey)
    if args.list_project:
        list_project(redmine)
        return
    if args.list_tracker:
        list_tracker(redmine)
        return

    # 日本語の時があるのでunicodeにする
    channel = args.channel.decode('utf8')
    username = args.username.decode('utf8')

    projects = args.projects
    issues = {}
    if len(projects) == 0:
        for p in redmine.project.all():
            issues.update(get_issues(p, args.days, args.tracker, args.ignore_nodate))
    else:
        for pid in projects:
            p = redmine.project.get(pid)
            issues.update(get_issues(p, args.days, args.tracker, args.ignore_nodate))

    if len(issues) > 0:
        post_slack(issues, username, channel)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
