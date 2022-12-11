import azure.functions as func
import logging
import json
from predict import implicit_predict, test_func


app = func.FunctionApp()

# Learn more at aka.ms/pythonprogrammingmodel

@app.function_name(name="HttpTrigger1")
@app.route(route="hello", auth_level=func.AuthLevel.ANONYMOUS)
def predict_function(req: func.HttpRequest) -> func.HttpResponse:
     logging.info('Python HTTP trigger function processed a request.')

     userid = req.params.get('userid')
     if not userid:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            userid = req_body.get('userid')

     if userid:
        try:
            userid = int(userid)
            recommendations = implicit_predict(userid)
        except Exception as e:
            return func.HttpResponse(status_code=500, body=e)
        return func.HttpResponse(json.dumps(recommendations))
     else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
