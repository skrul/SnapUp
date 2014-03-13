import httplib2

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials


class GoogleAnalytics(object):
    def __init__(self, service_account_name, private_key, profile_id):
        self._credentials = SignedJwtAssertionCredentials(
            service_account_name,
            private_key,
            scope='https://www.googleapis.com/auth/analytics.readonly')
        self._profile_id = profile_id
        self._service = None

    def _get_service(self):
        if not self._service:
            http = httplib2.Http()
            http = self._credentials.authorize(http)
            self._service = build(serviceName='analytics', version='v3',
                                  http=http)
        return self._service

    def date_query(self, start_date=None, end_date=None, metrics=None,
                   dimensions=None):
        service = self._get_service()
        data_query = service.data().ga().get(
            ids='ga:' + self._profile_id,
            start_date=start_date,
            end_date=end_date,
            dimensions=dimensions,
            metrics=metrics).execute()
        return data_query['rows']

    def realtime_query(self, metrics=None):
        service = self._get_service()
        data_query = service.data().realtime().get(
            ids='ga:' + self._profile_id,
            metrics=metrics).execute()
        return data_query['rows']
