def fetch_with_retries(magtag, action):
    succeeded = False
    while not succeeded:
        try:
            raw_data = magtag.fetch()
            return action(raw_data)
        except Exception as e:
            print('Sleeping before retrying: {}'.format(str(e)))
            magtag.enter_light_sleep(5.0)