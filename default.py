#!/usr/bin/env python
# vim: set ts=4 sw=4 et smartindent ignorecase fileencoding=utf8:

REDMINE_URL = None
REDMINE_KEY = None

# 何日前になったら通知するか
REDMINE_DAYS = 7

# 見るプロジェクトのID。リスト指定([1,2,...]全プロジェクトの場合は空([])
PROJECT_ID = []

# 参照するTrackerID。全部の場合はNone
TRACKER_ID = None

# Slack Incoming Webhook URL
SLACK_URL = None

# Slack User Name
SLACK_USERNAME = None

# Slack Channel
SLACK_CHANNEL = 'general'

# Slack eomji
SLACK_EMOJI = ':ghost:'
