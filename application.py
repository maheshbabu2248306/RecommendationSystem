from flask import Flask, render_template, request
from src.Components.model_development import ModelDevelopment


application = Flask(__name__)


@application.route("/")
def index():
    return "index page"


@application.route("/homepage", methods = ["GET", "POST"])
def homepage():
    if request.method == "POST":
        print("inside the post() before if method")
        if request.form.get("button") == "Search":
            print("Got into button search request block")
            val = request.form.get("recommendation")
            model_obj = ModelDevelopment()
            recommendations = model_obj.get_recommendations(val)
            
            length = len(recommendations)

            dict_names = [item["Title"] for item in recommendations]
            print("dict_names: ",dict_names)
            #print("length value is ", length)
            #print("recommendations value is ", recommendations)

            #return "<h2>{0} {1}</h2>".format(length, recommendations)
            if length == 0:
                length = -1
            
            return render_template("demofile1.html", length = length, dict_list = dict_names)
        else:
            print("inside the post before the else method")
            return render_template("demofile1.html")
    else:
        print("outside the else block")
        return render_template("demofile1.html")

if __name__ == "__main__":
    application.run(debug=False)
