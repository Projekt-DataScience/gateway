MICROSERVICES = {
   "backend-main" : {
      "url" : "http://web:8001/",
      "openapi_file" : "openapi.json",
      "fall_back" : False,
   },
   "frontend": {
      "url": "http://frontend:8000/",
      "openapi_file": "",
      "fall_back" : True,
   },
#   "backend-tasks" : {
#      "url" : "http://tasks:8000/",
#      "openapi_file" : "openapi.json",
#      "fall_back" : False,
#   },
#   "backend-audit": {
#      "url": "http://audit:8000/",
#      "openapi_file": "openapi.json",
#      "fall_back": False,
#   },
#   "backend-user-management": {
#      "url": "http://user-management:8000/",
#      "openapi_file": "openapi.json",
#      "fall_back": False,
#   },
}