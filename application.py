from flask import Flask, request, render_template
from src.pipeline.prediction_pipeline import CustomData, PredictPipeline
from src.exception import CustomException
from src.logger import logging
import mlflow

application = Flask(__name__)
app=application

@app.route('/')
def home_page():
    try:
        return render_template('form.html')
    except Exception as e:
        error_message = f'Error rendering form.html: {str(e)}'
        logging.error(error_message)
        raise CustomException(error_message)

@app.route('/predict', methods=['GET', 'POST'])
def predict_datapoint():
    try:
        if request.method == 'GET':
            return render_template('form.html')
        else:
            form_data = request.form
            data = CustomData(**form_data.to_dict())
            final_new_data = data.get_data_as_dataframe()
            predict_pipeline = PredictPipeline()
            pred = predict_pipeline.predict(final_new_data)
            results = pred[0]
            #print(f"prediction Results : {results}")

            if results == 0.0:
                answer = "EDIBLE"
            else:
                answer = "POISONOUS"

            return render_template('form.html', final_result=answer)
    except Exception as e:
        error_message = f'Exception occurred while running Flask API: {str(e)}'
        logging.error(error_message)
        raise CustomException(error_message)

if __name__ == "__main__":
    app.run(debug=True)