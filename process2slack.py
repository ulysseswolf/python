#!/usr/bin/env python

import requests
from requests import post
from json import dumps
from lxml import etree

id = '18293812312345123'
slack_webhook = 'slack incoming webhook url'


payload = {'keyword': id, 'action': 'query'}
source = requests.get("http://info.szhr.com:9001/public/agentProgQuery.jsp?", params = payload)

html = etree.HTML(source.content)

status = html.xpath('//*[@id="content"]/div/table/tbody/tr/td/text()[4]')[0]
notice = html.xpath('//*[@id="content"]/div/table/tbody/tr/td/text()[6]')[0]

webhook = post(slack_webhook, {
    'payload': dumps({
        'attachments':[
            {
                'fallback': 'process',
                'pretext': 'process',
                'color': "#36a64f",
                'title': status,
                'title_link': source.url,
                'text': notice
            }
        ]
    })
})
