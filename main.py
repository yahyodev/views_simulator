try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    import time
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    import random
    from multiprocessing import Process
    from lists import PROXIES, USER_AGENTS, VIDEOS

    window_sizes = ['1024,640', '1366,768', '1920,1080', '1536,864', '1440,900', '1280,720', '1600,900', '1280,800',
                    '1280,1024', '1024,768', '768,1024']
    videos = VIDEOS
    user_agents = USER_AGENTS
    proxies = PROXIES
    options = Options()
    options.add_argument('--profile-directory=Default')
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")
    options.add_argument("--mute-audio")
    options.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})
    options.add_experimental_option('useAutomationExtension', False)


    def scrape():
        while True:
            time.sleep(random.randint(1, 5))

            global options
            global webdriver
            options.add_argument(f"--window-size={window_sizes[random.randint(0, len(window_sizes) - 1)]}")
            options.add_argument('--start-maximized')

            if proxies:
                proxy = proxies[random.randint(0, len(proxies) - 1)]
                options.add_argument('--proxy-server=%s' % proxy)
                webdriver.DesiredCapabilities.CHROME['proxy'] = {
                    "httpProxy": f'http://{proxy}',
                    "ftpProxy": f'http://{proxy}',
                    "sslProxy": f'http://{proxy}',
                    "proxyType": "MANUAL",

                }
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.delete_all_cookies()
            driver.execute_cdp_cmd('Network.setUserAgentOverride',
                                   {
                                       "userAgent": user_agents[random.randint(0, len(user_agents) - 1)]
                                   })
            driver.refresh()
            driver.get(videos[random.randint(0, len(videos) - 1)])
            action = ActionChains(driver)
            action.send_keys(Keys.SPACE)
            action.perform()
            time.sleep(random.randint(25, 120))
            print('successful')

    for _ in range(2):
        Process(target=scrape).start()
except:
    print(Exception)
