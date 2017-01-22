# -*- coding: utf-8 -*-

import random
import datetime
import guokeSpider.user_agents as user_agents

random.seed(datetime.datetime.now())
class UserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(user_agents.agents)
        request.headers['User-Agent'] = agent