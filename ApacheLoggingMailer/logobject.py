class LogObject:
     def __init__(self, ip_address, date, request, status_code, host_address, client_info):
         self.ip_address = ip_address
         self.date = date
         self.request = request
         self.status_code = status_code
         self.host_address = host_address
         self.client_info = client_info