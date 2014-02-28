# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# -*- coding: utf-8 -*-

#Experimental Mechanize Build for Python 3 GH: /adevore/mechanize/tree/python3
import mechanize
import http.cookiejar

class AnonymousBrowser(mechanize.Browser):
    """ Anonymous browser tool extending programmatic web browser mechanize
        to prevent request limits put in by the content providers while scraping
    """
    def __init__(self, proxies=None, user_agents=None):
        #Since lists are mutable objects it would be 
        #dangerous to use as a default argument
        if proxies is None:
            proxies = []
        if user_agents is None:
            user_agents = []

        mechanize.Browser.__init__(self)
        self.set_handle_robots(False)
        self.proxies = proxies
        self.user_agents = user_agents + ['Mozilla/5.0',
                                          'Opera/9.52',
                                          'Chrome/28.0.1467.0',
                                          ]

        self.cookie_jar = http.cookiejar.LWPCookieJar()

        self.set_cookiejar(self.cookie_jar)

        self.anonymize()

    def clear_cookies(self):
        self.cookie_jar = http.cookiejar.LWPCookieJar()
        self.set_cookiejar(self.cookie_jar)

    def change_user_agent(self):
        """Change the user agent header used to a random one"""
        random_user_agent = choice(self.user_agents)
        self.addheaders = [('User-agent', random_user_agent)]

    def change_proxy(self):
        """Change the proxy used to a random one"""
        if self.proxies:
            random_proxy = choice(self.proxies)
            self.set_proxies({'http': random_proxy})

    def anonymize(self):
        self.clear_cookies()
        self.change_user_agent()
        self.change_proxy()

