from gmail_service import GmailService


class EmailServices:

    def __init__(self):
        self.services = []
        self.services.append(('gmail', GmailService()))

    def get_service_types(self):
        result = []
        for service in self.services:
            result.append(service[0])
        return result

    def get_service(self, type):
        for service in self.services:
            if service[0] == type:
                return service[1]

        raise Exception("Unsupported email service type")
