from src.classes.requesters.base_requester import BaseRequester


class ZeepRequester(BaseRequester):
    """Class realize request using zeep library"""

    def _get_request_json(self) -> dict:
        pass
        # session = requests.session()
        # session.headers = self.payload['headers']
        #
        # response = session.request(
        #     method=self.payload['method'],
        #     url=self.payload['url'],
        #     data=self.payload['data'].encode('utf-8'),
        #     verify=False,
        # )
        # logger.debug((response.status_code, response.content))
        # return {'status': response.status_code, 'content': response.content}

    async def send_request(self) -> dict:
        return self._get_request_json()
