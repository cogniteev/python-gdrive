import logging

import requests


LOGGER = logging.getLogger(__name__)


class GoogleDrive(object):
    """ A simple API wrapper for google drive

    """

    def __init__(self, token, refresh_token, client_id, client_secret,
                 refresh_callback=None):
        """

        :param token: the granted access token
        :param refresh_token: the granted refresh token
        :param client_id: Oauth client id
        :param client_secret: Oauth client secret
        :param refresh_callback: callable to handle credentials refreshing
        """
        self.token = token
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_callback = refresh_callback

    def __refresh_token(self):
        """ Handles the refresh process and update with newly acquired values

        """
        refresh_data = {
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token'
        }

        response = requests.post('https://accounts.google.com/o/oauth2/token',
                                 data=refresh_data).json()

        self.token = response['access_token']

        if self.refresh_callback:
            self.refresh_callback(self.token, self.refresh_token)

    def __token_header(self):
        """ Create an HTTP header containing the access token


        :return: the properly formatted header
        """
        return {'Authorization': 'Bearer {token}'.format(token=self.token)}

    def __request(self, method, path, params=None, refreshed=False):
        """ submit a request to the google drive API server

        :param method: HTTP verb to use
        :param path: REST resource's path
        :param params: parameters for the request
        :param refreshed: True if the call is made after a token refresh
        :return: Server's raw response
        """
        url = 'https://www.googleapis.com/drive/v2/{path}'.format(path=path)

        headers = self.__token_header()

        response = requests.request(method, url, params=params, headers=headers)

        if response.status_code == 401:
            if refreshed:
                return response
            self.__refresh_token()
            return self.__request(method, path, refreshed=True)
        else:
            return response

    def download(self, url, refreshed=False, file_id=None):
        """ download a file content

        :param str url:
          the url to download the file from
        :param bool refreshed:
          True if the call is made after a token refresh
        :param str file_id:
          optional file identifier used to retrieve a new download url when
          the one specified has expired.

        :return: file's content
        """
        headers = self.__token_header()

        response = requests.request('get', url, headers=headers, stream=True)

        if response.status_code == 401:
            if refreshed:
                return response
            self.__refresh_token()
            return self.download(url, refreshed=True)

        if response.status_code == 403 and file_id is not None:
            # downloadUrl link has expired, get a new one
            file_desc = self.get_file(file_id)
            if file_desc.status_code == 200:
                return self.download(
                    file_desc.json().get('downloadUrl'),
                    file_id=None,
                    refreshed=refreshed
                )
            else:
                msg = (u'Could not retrieve file description: {file_id}'
                       ': {status_code} {response}')
                LOGGER.error(msg.format(
                    file_id=file_id,
                    status_code=file_desc.status_code,
                    response=file_desc.text
                ))
        return response

    def get_file(self, file_id):
        """ Retrieve file description

        :param str file_id: file identifier
        :return: Server's raw response
        """
        return self.__request('get', u'files/{}'.format(file_id))

    def get_user_files(self, count=100, page_token=None):
        """ Retrieve user's files metadata

        :param count: number of file to get
        :param page_token: optional, page token pagination parameter
        :return: Server's raw response
        """
        params = {
            'q': "mimeType != 'application/vnd.google-apps.folder'",
            'maxResults': count,
            'pageToken': page_token
        }
        return self.__request('get', 'files', params=params)

    def get_user_files_generator(self, count=100):
        """ Create a generator to iterate through user's files

        :param count: number of files metadata to get at each iteration
        """
        next_page_token = None
        while True:
            response = self.get_user_files(count=count,
                                           page_token=next_page_token).json()
            next_page_token = response.get('nextPageToken', None)
            for item in response.get('items', []):
                yield item

            if not next_page_token:
                break

    def get_file_comments(self, file_id, count=100, page_token=None):
        """ Retrieve a list of comments for a given file

        :param file_id: the file to get associated comments
        :param count: number of comments to get
        :param page_token: page token pagination parameter
        :return: Server's raw response
        """
        params = {
            'maxResults': count,
            'pageToken': page_token
        }
        return self.__request('get', 'files/{id}/comments'.format(id=file_id),
                              params=params)

    def get_file_comments_generator(self, file_id, count=100):
        """ Create a generator to iterate through comments

        :param file_id: the file to get associated comments
        :param count: number of comments to get at each iteration
        """
        next_page_token = None
        while True:
            response = self.get_file_comments(file_id, count=count,
                                              page_token=next_page_token).json()
            next_page_token = response.get('nextPageToken', None)
            for item in response.get('items', []):
                yield item

            if not next_page_token:
                break
