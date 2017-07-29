from gmail_service import GmailService


class EmailServices:
    def __init__(self):
        self.field = None

    @staticmethod
    def get_service_types():
        return ['gmail']

    @staticmethod
    def get_service(type, credentials):
        if type == 'gmail':
            return GmailService(credentials)
        else:
            raise Exception("Unsupported email service type")
